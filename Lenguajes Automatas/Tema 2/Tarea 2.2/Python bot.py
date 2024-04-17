import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresión regular para detectar mensajes que contienen "Hola"
expresion_regular = re.compile(r"hello|hi|hola", re.IGNORECASE)

Mensaje = re.compile(r"Enviar mensaje|envia mensaje|envia un mensaje", re.IGNORECASE)

patron_origen_destino_fecha = r"volar de (\w+) a (\w+) el (\d{1,2} de \w+)"
patron_precio = r"cuánto cuesta un vuelo de (\w+) a (\w+)"
patron_ida_vuelta = r"un vuelo de ida y vuelta de (\w+) a (\w+)"

Aviso = r"Dile a ([\w\s]+) que (.+) a las (([01]?[0-9]|2[0-3]):[0-5][0-9])"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message if it matches the regular expression."""
    message_text = update.message.text
    if expresion_regular.search(message_text):
        await update.message.reply_text("¡Hola! ¿Cómo estás?")
    elif Mensaje.search(message_text):
        await update.message.reply_text("Hola Ema que tal tu dia.")
    if re.search(patron_origen_destino_fecha, message_text):
        origen_destino_fecha = re.search(patron_origen_destino_fecha, message_text)
        origen = origen_destino_fecha.group(1)
        destino = origen_destino_fecha.group(2)
        fecha = origen_destino_fecha.group(3)
        await update.message.reply_text(f"Buscar vuelo de {origen} a {destino} para el {fecha}")
    elif re.search(patron_precio, message_text):
        precio = re.search(patron_precio, message_text)
        origen = precio.group(1)
        destino = precio.group(2)
        await update.message.reply_text(f"Consultar precio de vuelo de {origen} a {destino}")
    elif re.search(patron_ida_vuelta, message_text):
        ida_vuelta = re.search(patron_ida_vuelta, message_text)
        origen = ida_vuelta.group(1)
        destino = ida_vuelta.group(2)
        await update.message.reply_text(f"Buscar vuelo de ida y vuelta de {origen} a {destino}")
    elif re.search(Aviso, message_text):
        Anuncio = re.search(Aviso, message_text)
        destinatario = Anuncio.group(1)
        mensaje = Anuncio.group(2)
        hora = Anuncio.group(3)
        await update.message.reply_text(f"Se informo a {destinatario} que {mensaje} a las {hora}")
    else:
        await update.message.reply_text("No entendí tu mensaje.")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token("7178908011:AAH9y4C2YgUTY_gBhDmMwBwCf4u8aXTKknU").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
