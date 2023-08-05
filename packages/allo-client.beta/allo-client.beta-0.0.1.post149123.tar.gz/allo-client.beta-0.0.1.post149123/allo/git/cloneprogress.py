#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import progressbar
from git import RemoteProgress


class CloneProgress(RemoteProgress):
    bar = None
    max = 0
    format_custom_text = progressbar.FormatCustomText('%(message)s', dict(message=''))
    widgets = [
        'Téléchargement du logiciel: ', progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', format_custom_text,
    ]

    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count is not None and self.bar is None or max_count > self.max:
            self.max = max_count
            self.bar = progressbar.ProgressBar(max_value=max_count, widgets=self.widgets)
        elif self.bar is not None:
            self.bar.update(cur_count)
        self.format_custom_text.update_mapping(message=message)
