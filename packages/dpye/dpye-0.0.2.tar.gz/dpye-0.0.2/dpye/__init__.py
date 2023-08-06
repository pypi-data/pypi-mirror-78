def add_client():
	import discord
	from discord.ext import commands
	client = commands.Bot(command_prefix = prefix, help_command = None, case_insensitive=True)

def clear():
	async def clear(ctx, a:int):
		await ctx.channel.purge(limit=a)
		await ctx.channel.send(embed=discord.Embed(color=0xFF0000, description=f'Успешно очищено {a} сообщений'))
def run():
	client.run