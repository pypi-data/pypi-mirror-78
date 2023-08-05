import pytest

from huscy.subjects.services import create_note
from huscy.subjects.models import Note

pytestmark = pytest.mark.django_db


def test_create_note(subject, user):

    assert subject.notes.count() == 0

    note_option = Note.OPTIONS.get_value('hard_of_hearing')
    note_text = 'here is text'
    create_note(subject, user, note_option, note_text)

    assert subject.notes.count() == 1
    assert subject.notes.get().text == ''


def test_create_note_with_custom_text(subject, user):

    assert subject.notes.count() == 0

    note_option = Note.OPTIONS.get_value('other')
    note_text = 'here is text'
    create_note(subject, user, note_option, note_text)

    assert subject.notes.count() == 1
    assert subject.notes.get().text == note_text
