from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_wallet, store_wallet
from wallet import create_wallet
from config import RPC_URL
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.async_api import AsyncClient
import base58

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallet = get_user_wallet(user_id)

    if not wallet:
        public_key, private_key = create_wallet()
        store_wallet(user_id, public_key, private_key)
        await update.message.reply_text(
            f"Welcome! A new Solana wallet has been created for you.\n\n"
            f"Public Key: {public_key}"
        )
    else:
        public_key = wallet[0]
        await update.message.reply_text(
            f"Welcome back! Here is your Solana wallet info:\n\n"
            f"Public Key: {public_key}"
        )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallet = get_user_wallet(user_id)

    if not wallet:
        await update.message.reply_text("You don't have a wallet yet. Use /start to create one.")
        return

    public_key_str = wallet[0]
    try:
        public_key = Pubkey.from_string(public_key_str)
        async with AsyncClient(RPC_URL) as client:
            response = await client.get_balance(public_key)
            balance = response.value / 1e9  # Convert lamports to SOL
            await update.message.reply_text(f"Your wallet balance is {balance:.4f} SOL.")
    except Exception as e:
        await update.message.reply_text(f"There was an error checking your balance: {str(e)}")

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallet = get_user_wallet(user_id)

    if not wallet:
        await update.message.reply_text("You don't have a wallet yet. Use /start to create one.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /send <recipient_public_key> <amount>")
        return

    recipient_public_key_str = context.args[0]
    amount = context.args[1]
    try:
        amount_lamports = int(float(amount) * 1e9)  # Convert SOL to lamports
        sender_public_key = Pubkey.from_string(wallet[0])
        sender_private_key = base58.b58decode(wallet[1])
        recipient_public_key = Pubkey.from_string(recipient_public_key_str)

        sender_keypair = Keypair.from_bytes(sender_private_key)

        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=sender_public_key,
                to_pubkey=recipient_public_key,
                lamports=amount_lamports
            )
        )
        transaction = Transaction().add(transfer_instruction)

        async with AsyncClient(RPC_URL) as client:
            blockhash_resp = await client.get_latest_blockhash()
            transaction.recent_blockhash = blockhash_resp.value.blockhash
            transaction.sign([sender_keypair])
            send_resp = await client.send_transaction(transaction)

            if send_resp.value:
                await update.message.reply_text(f"Transaction successful! Signature: {send_resp.value}")
            else:
                await update.message.reply_text("Transaction failed. Please try again.")
    except Exception as e:
        await update.message.reply_text(f"There was an error sending SOL: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here are the commands you can use:\n"
        "/start - Welcome message and create/check your Solana wallet\n"
        "/help - List available commands\n"
        "/balance - Check the balance of your Solana wallet\n"
        "/send <recipient_public_key> <amount> - Send SOL to another wallet"
    )