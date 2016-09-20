# -*- coding: utf-8 -*-


import django
from django.test import TestCase

from django.core.urlresolvers import reverse

from datetime import datetime
from app.forms import MemberForm


class MainPageForms(TestCase):
    """ Main page forms test"""

    def setUp(self):
        self.form = MemberForm()

    #def test_member_form(self):
    #    self.form = MemberForm()        
    #    self.assertContains(self.form, u"""<div class="modal-footer">                            
    #                                        <input type="submit" name="save" value="Готово" class="btn btn-primary">              
    #                                        <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
    #                                 </div>""")
        