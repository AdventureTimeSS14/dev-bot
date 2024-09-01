import discord

from config import AUTHOR, GLOBAL_SESSION, REPOSITORIES, WHITELIST_ROLE_ID


async def validate_user(ctx):
    """Checks if the user has the correct role to use the command."""
    if not any(role.id in WHITELIST_ROLE_ID for role in ctx.author.roles):
        await ctx.send("Не могу идентифицировать вас в базе данных команды разработки Adventure Time, вы не имеете права пользоваться этой командой.")
        return False
    return True


async def validate_repository(ctx, repo_key):
    """Validates the provided repository key."""
    if repo_key not in REPOSITORIES:
        await ctx.send("Пожалуйста, укажите корректный репозиторий: n или o.")
        return None
    return f"{AUTHOR}/{REPOSITORIES[repo_key]}"


async def fetch_github_data(url, params=None):
    """Fetches data from GitHub API."""
    try:
        response = GLOBAL_SESSION.get(url, params=params)
        if response.status_code != 200:
            print(f"Error while fetching data from GitHub: {response.status_code}")
            return None
        return response.json()
    except Exception as e:
        print(f"Error when making a request to the GitHub API: {e}")
        return None


async def create_embed_list(title, items, color, formatter, max_items_per_embed=25):
    """Creates a list of embeds from the fetched data."""
    embed_list = []
    current_embed = discord.Embed(title=title, color=color)

    for i, item in enumerate(items):
        if i % max_items_per_embed == 0 and i > 0:
            embed_list.append(current_embed)
            current_embed = discord.Embed(title=title, color=color)
        current_embed.add_field(**formatter(item))

    embed_list.append(current_embed)
    return embed_list


async def send_embeds(ctx, embed_list):
    """Sends a list of embeds to the Discord channel."""
    for embed in embed_list:
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException as exc:
            await ctx.send(f"Ошибка отправки сообщения: {exc}")
