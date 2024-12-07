import discord


class Verify_button(discord.ui.View):
    def __init__(self, title: str, description: str):
        super().__init__(timeout=None)
        self.title = title
        self.description = description
        return

    @discord.ui.button(label=ti)