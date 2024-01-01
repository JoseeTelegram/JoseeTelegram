from aiogram import types

note = {}

async def cmd_note(msg: types.Message) -> None:
  arg = msg.text.split()[1:]

  if not arg:
    await msg.reply("Usage: /note <add/list/delete> <note>")
    return
  
  notes = open("tg_bot/data/notes.json", "r+")

  if notes.read == "":
    notes.write("{}")
  
  if arg[0] == "add":
    if len(arg) == 1:
      await msg.reply("Nothing to note here...")
      return
    note[str(msg.chat.id)].append(" ".join(arg[1:]))
    await msg.reply("Note succesfully created.")
    return

  elif arg[0] == "list":
    if not note[str(msg.chat.id)]:
      await msg.reply("You have no notes, to create new: /note add <note>")
      return
    answer = "*Note List*\n"
    for i in range(0, len(note[str(msg.chat.id)])):
      answer += f"{i+1}. {note[str(msg.chat.id)][i]}\n"
    await msg.reply(answer, parse_mode = 'Markdown')
    return
    
  elif arg[0] == "delete":
    if arg[1].isdigit():
      if int(arg[1]) == 0 or int(arg[1])-1 > len(note[str(msg.chat.id)]):
        await msg.reply("That note already doesn't exists.")
        return
      del note[str(msg.chat.id)][int(arg[1])-1]
      await msg.reply("Note succesfully deleted.")
      return
    elif arg[1] == "all":
      note[str(msg.chat.id)].clear()
      await msg.reply("All notes was deleted.")
      return
    else:
      await msg.reply("Usage: /note delete <number/\"all\">")
      return
  
  else:
    await msg.reply("Usage: /note <add/list/delete> <note>")
    return
