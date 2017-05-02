#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot

from src.database import Database
from src.utilities import valid_roll, roll_to_val

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class DMAssistant:
    def __init__(self, token, dm_id):
        self.db = Database('rolls.db')
        self.dm = dm_id

        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.handle)

    def handle(self, msg):
        msg_type, chat_type, chat_id = telepot.glance(msg)

        if msg_type != 'text':
            return

        user_input = msg['text'].strip().split()
        command = user_input[0]
        who = msg['from']['id']
        caster = msg['from']['first_name']
        print msg['from']
        text = ''

        if who == self.dm and (command == '/add_roll' or command == '/add_roll@DMAssistant'):
            if len(user_input) != 3:
                text = 'The right use is :\n*/add_roll shortcut roll*'
            else:
                if self.db.add_shortcut(user_input[1], user_input[2]):
                    text = 'The shortcut was correctly added.'
                else:
                    text = 'There was a problem adding the shortcut.'

        elif who == self.dm and (command == '/remove_roll' or command == '/remove_roll@DMAssistant'):
            if len(user_input) != 2:
                text = 'The right use is :\n*/remove_roll shortcut*'
            else:
                if self.db.remove_shortcut(user_input[1]):
                    text = 'The shortcut was correctly removed.'
                else:
                    text = 'There was a problem removing the shortcut.'

        elif command == '/roll' or command == '/roll@DMAssistant':
            if len(user_input) != 2:
                text = 'The right use is :\n*/roll shortcut*'
            else:
                value = self.db.apply_shortcut(user_input[1])
                if value is not None:
                    text = '*' + caster + ' rolled ' + str(value) + '*'
                else:
                    text = 'That shortcut does not exists.'

        elif command == '/roll_now' or command == '/roll_now@DMAssistant':
            if len(user_input) != 2:
                text = 'The right use is :\n*/roll_now roll*'
            else:
                roll = user_input[1]
                if valid_roll(roll):
                    text = '*' + caster + ' rolled ' + str(roll_to_val(roll)) + '*'
                else:
                    text = 'There was a problem with you input.'
        elif command == '/show_rolls' or command == '/show_rolls@DMAssistant':
            if len(user_input) != 1:
                text = 'The right use is :\n*/show_rolls*'
            else:
                shortcuts = self.db.get_shortcuts()
                text = 'The following rolls are available:\n\n'
                for shortcut, roll in shortcuts:
                    text += shortcut + ' - ' + roll + '\n'

        if text != '':
            self.bot.sendMessage(chat_id, text, 'Markdown')
