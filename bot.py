import toml
import platform
import subprocess
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Read secrets from secrets.toml
with open(".streamlit/secrets.toml", "r") as f:
    secrets = toml.load(f)

BOT_TOKEN = secrets["BOT_TOKEN"]

def get_system_info():
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    return (
        f"System: {system}\n"
        f"Release: {release}\n"
        f"Version: {version}\n"
        f"Machine: {machine}\n"
        f"Processor: {processor}"
    )

async def start(update, context):
    sysinfo = get_system_info()
    await update.message.reply_text(
        f"Hello! I'm your simple Telegram bot.\n\n"
        f"System Information:\n{sysinfo}"
    )

async def echo(update, context):
    await update.message.reply_text(update.message.text)

async def cmd(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /cmd <command>")
        return

    cmd_text = " ".join(context.args)
    system = platform.system()

    if system == "Windows":
        shell_cmd = ["cmd.exe", "/C", cmd_text]
    else:
        shell_cmd = ["/bin/bash", "-c", cmd_text]

    try:
        result = subprocess.run(shell_cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "No output."
        elif len(output) > 4000:
            output = output[:4000] + "\n\n(Output truncated)"
        await update.message.reply_text(f"```\n{output}\n```", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cmd", cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
