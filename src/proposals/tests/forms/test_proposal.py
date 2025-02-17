import pytest

from proposals.forms import (
    TalkProposalCancelForm, TutorialProposalCancelForm,
    TalkProposalCreateForm, TutorialProposalCreateForm,
    TalkProposalUpdateForm, TutorialProposalUpdateForm,
)
from proposals.models import TalkProposal, TutorialProposal


@pytest.fixture
def talk_proposal_data():
    return {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF15',
        'language': 'ENEN',
        'talk_language': 'en',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'live_stream_policy': True,
        'referring_policy': True,
        'first_time_speaker': True,
        'living_in_taiwan': True,
        'pre_recorded_policy': True,
        'prefer_time': 'DAY_ONE_MORNING',
    }


def test_talk_proposal_create_form():
    form = TalkProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'talk_language', 'python_level',
        'recording_policy', 'live_stream_policy', 'first_time_speaker', 'referring_policy',
        'prefer_time', 'living_in_taiwan', 'pre_recorded_policy',
    ]


def test_talk_proposal_create_form_no_request(talk_proposal_data):
    form = TalkProposalCreateForm(data=talk_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Talk proposal creation requires a request object.'],
    }


def test_talk_proposal_create_form_invalid_user(
        talk_proposal_data, request, invalid_user):
    request.user = invalid_user
    form = TalkProposalCreateForm(request=request, data=talk_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'create a talk proposal.',
        ],
    }


def test_talk_proposal_create_form_valid(talk_proposal_data, request, user):
    request.user = user
    form = TalkProposalCreateForm(request=request, data=talk_proposal_data)
    assert form.is_valid()


@pytest.fixture
def tutorial_proposal_data():
    return {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'ENEN',
        'talk_language': 'en',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'live_stream_policy': True,
        'living_in_taiwan': True,
        'pre_recorded_policy': True,
        'prefer_time': 'DAY_ONE_MORNING',
    }


def test_tutorial_proposal_create_form():
    form = TutorialProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'talk_language',
        'python_level', 'recording_policy', 'live_stream_policy',
        'prefer_time', 'living_in_taiwan', 'pre_recorded_policy',
    ]


def test_tutorial_proposal_create_form_no_request(tutorial_proposal_data):
    form = TutorialProposalCreateForm(data=tutorial_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Tutorial proposal creation requires a request object.'],
    }


def test_tutorial_proposal_create_form_anonymous(
        tutorial_proposal_data, request, invalid_user):
    request.user = invalid_user
    form = TutorialProposalCreateForm(
        request=request, data=tutorial_proposal_data,
    )
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'create a tutorial proposal.',
        ],
    }


def test_tutorial_proposal_create_form_valid(
        tutorial_proposal_data, request, user):
    request.user = user
    form = TutorialProposalCreateForm(
        request=request, data=tutorial_proposal_data,
    )
    assert form.is_valid()


def test_talk_proposal_update_form():
    form = TalkProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'talk_language',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy',
        'live_stream_policy', 'first_time_speaker', 'slide_link',
    ]


def test_tutorial_proposal_update_form():
    form = TutorialProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'talk_language',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy',
        'live_stream_policy', 'slide_link',
    ]


@pytest.mark.parametrize('form_class', [
    TalkProposalCancelForm, TutorialProposalCancelForm,
])
def test_proposal_cancel_form_no_instance(form_class):
    with pytest.raises(ValueError) as ctx:
        form_class()
    assert str(ctx.value) == (
        'Proposal cancel form must be initialized with an instance.'
    )


def test_talk_proposal_cancel_form(talk_proposal):
    form = TalkProposalCancelForm(instance=talk_proposal)
    assert list(form.fields) == ['cancelled']


def test_tutorial_proposal_cancel_form(tutorial_proposal):
    form = TutorialProposalCancelForm(instance=tutorial_proposal)
    assert list(form.fields) == ['cancelled']


def test_talk_proposal_cancel_form_save(talk_proposal):
    assert not talk_proposal.cancelled
    form = TalkProposalCancelForm(
        data={'cancelled': 'true'}, instance=talk_proposal,
    )
    form.save()
    assert TalkProposal.objects.get(pk=talk_proposal.pk).cancelled


def test_tutorial_proposal_cancel_form_save(tutorial_proposal):
    assert not tutorial_proposal.cancelled
    form = TutorialProposalCancelForm(
        data={'cancelled': 'true'}, instance=tutorial_proposal,
    )
    form.save()
    assert TutorialProposal.objects.get(pk=tutorial_proposal.pk).cancelled
