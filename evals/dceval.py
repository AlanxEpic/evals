import re, os, random, asyncio, logging, time, requests, io, sys, traceback

async def deval(client, message):
    status_message = await message.channel.send("**•×• Processing... •×•**")
    cmd = message.content.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reference:
        reply_to_ = await message.channel.fetch_message(message.reference.message_id)

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**•• Eᴠᴀʟ ••\n** "
    final_output += f"`{cmd}`\n\n"
    final_output += "**•• Oᴜᴛᴘᴜᴛ ••** \n"
    final_output += f"`{evaluation.strip()}` \n"

    if len(final_output) > 1900:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply(file=discord.File(out_file, filename=out_file.name))
            print(evaluation.strip())
    else:
        await status_message.edit(content=final_output)
        print(evaluation.strip())

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
