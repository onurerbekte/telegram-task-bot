"""Kurgusal demo proje / Fictional demo project: private-chat task bot."""
import argparse
import asyncio
import os
from types import SimpleNamespace
from telegram.ext import Application, CommandHandler
from store import TaskStore

COPY={
    "tr":{"help":"Kurgusal demo proje.\n/add görev — ekle (1–200 karakter)\n/list — son 10 kayıt\n/done id — tamamla\n/delete id — sil\n/lang tr veya en\nKullanıcı başına en fazla 100 kayıt.","private":"Bu bot yalnızca özel sohbetlerde çalışır / Private chats only.","added":"Görev eklendi", "empty":"Henüz görev yok.","missing":"Kayıt yok, sana ait değil veya zaten tamamlandı.","updated":"Görev güncellendi.","deleted":"Görev silindi.","usage":"Geçerli görev veya sayısal kimlik gir. /help", "language":"Dil Türkçe oldu.","error":"İşlem tamamlanamadı. Tekrar dene."},
    "en":{"help":"Fictional demo project.\n/add task — add (1–200 characters)\n/list — last 10 entries\n/done id — complete\n/delete id — delete\n/lang tr or en\nUp to 100 entries per user.","private":"Bu bot yalnızca özel sohbetlerde çalışır / Private chats only.","added":"Task added", "empty":"No tasks yet.","missing":"Entry missing, not yours, or already completed.","updated":"Task updated.","deleted":"Task deleted.","usage":"Enter a valid task or numeric ID. /help", "language":"Language set to English.","error":"Operation failed. Please try again."}
}


def handler_for(store,command):
    async def handler(update,context):
        if not update.effective_message or not update.effective_user:return
        message=update.effective_message
        if not update.effective_chat or update.effective_chat.type!="private":
            await message.reply_text(COPY["tr"]["private"]);return
        user=update.effective_user.id
        t=COPY[store.language(user)]
        args=context.args or []
        try:
            if command in ("start","help"):
                reply=t["help"]
            elif command=="add":
                task_id=store.add(user," ".join(args));reply=f"{t['added']}: #{task_id}"
            elif command=="list":
                tasks=store.list(user)
                reply="\n".join(f"{'✓' if task['done'] else '○'} #{task['id']} {task['title']}" for task in tasks) or t["empty"]
            elif command in ("done","delete"):
                if len(args)!=1 or not args[0].isdigit():raise ValueError("Invalid id")
                changed=store.change(user,int(args[0]),delete=command=="delete")
                reply=t["deleted" if command=="delete" else "updated"] if changed else t["missing"]
            elif command=="lang":
                if len(args)!=1 or args[0] not in COPY:raise ValueError("Invalid language")
                store.set_language(user,args[0]);reply=COPY[args[0]]["language"]
            else:
                reply=t["help"]
        except ValueError:
            reply=t["usage"]
        await message.reply_text(reply)
    return handler


def build_application(token,store):
    application=Application.builder().token(token).build()
    for command in ("start","help","add","list","done","delete","lang"):
        application.add_handler(CommandHandler(command,handler_for(store,command)))
    async def on_error(update,context):
        # Never log exceptions containing token-bearing request URLs.
        if update and update.effective_message:
            await update.effective_message.reply_text("İşlem tamamlanamadı / Operation failed.")
    application.add_error_handler(on_error)
    return application


async def demo(store):
    async def reply(text):print(text)
    update=SimpleNamespace(effective_user=SimpleNamespace(id=1),effective_chat=SimpleNamespace(type="private"),effective_message=SimpleNamespace(reply_text=reply))
    for command,args in (("start",[]),("add",["Kurgusal","demo","görev"]),("list",[]),("lang",["en"]),("list",[])):
        await handler_for(store,command)(update,SimpleNamespace(args=args))


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--demo",action="store_true");args=parser.parse_args()
    if args.demo:
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            asyncio.run(demo(TaskStore(os.path.join(temp,"demo.sqlite"))))
        return
    token=os.getenv("TELEGRAM_BOT_TOKEN","").strip()
    if not token:parser.exit(1,"TELEGRAM_BOT_TOKEN gerekli / required. Use --demo for offline mode.\n")
    build_application(token,TaskStore(os.getenv("TASK_DATABASE","data/tasks.sqlite"))).run_polling()


if __name__=="__main__":main()
