from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import (
    Ability,
    Card,
    CardStage,
    CardType,
    Collection,
    Illustrator,
    Move,
    Rarity,
    User,
)


### User Registration ###   # noqa: E266
class SignUpForm(UserCreationForm):
    """Form for creating a new user."""

    username = forms.CharField(max_length=16, required=True)
    email = forms.EmailField(max_length=128, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the FormHelper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="form-group col-md-6 mb-0"),
                Column("email", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("password1", css_class="form-group col-md-6 mb-0"),
            ),
            Row(Submit("submit", "Sign Up", css_class="btn btn-primary")),
        )
        self.helper.form_method = "post"
        self.helper.form_class = "form"


class SignInForm(AuthenticationForm):
    """Form for logging in a user."""

    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the FormHelper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "username", css_class="form-group col-12 col-md-6 mb-3"
                ),  # noqa: E501
                Column(
                    "password", css_class="form-group col-12 col-md-6 mb-3"
                ),  # noqa: E501
                css_class="form-row",
            ),
        )
        self.helper.form_method = "post"
        self.helper.form_class = "form"


### Manage Cards ###   # noqa: E266
class AddAbilityForm(forms.ModelForm):
    """Form for adding a new ability."""

    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Ability
        fields = (
            "name",
            "description",
        )


class AddMoveForm(forms.ModelForm):
    """Form for adding a new move."""

    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Move
        fields = (
            "name",
            "description",
        )


class AddIllustratorForm(forms.ModelForm):
    """Form for adding a new illustrator."""

    name = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Illustrator
        fields = ("name",)


class AddProfilePictureForm(forms.ModelForm):
    """Form for adding a new profile picture."""

    image = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ("image",)


class AddCollectionForm(forms.ModelForm):
    """Form for adding a new collection."""

    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Collection
        fields = (
            "name",
            "description",
        )


class AddCardForm(forms.ModelForm):
    """Form for adding a new card."""

    name = forms.CharField(max_length=16, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    rarity = forms.ModelChoiceField(
        queryset=Rarity.objects.all(), required=True
    )
    card_type = forms.ModelChoiceField(
        queryset=CardType.objects.all(), required=True
    )
    card_stage = forms.ModelChoiceField(
        queryset=CardStage.objects.all(), required=True
    )
    abilities = forms.ModelMultipleChoiceField(
        queryset=Ability.objects.all(), required=False
    )
    moves = forms.ModelMultipleChoiceField(
        queryset=Move.objects.all(), required=False
    )

    class Meta:
        model = Card
        fields = (
            "name",
            "description",
            "rarity",
            "card_type",
            "card_stage",
            "abilities",
            "moves",
        )
        widgets = {
            "abilities": forms.CheckboxSelectMultiple,
            "moves": forms.CheckboxSelectMultiple,
        }
