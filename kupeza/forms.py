from django import forms
from .models import MyUser, Agencie, Countrie, Agency
from  .admin import UserCreationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['Select_Your_Agency'] = forms.ChoiceField( required= False,
            choices=[(o.id, str(o)) for o in Agencie.objects.all()]
        )

    package = forms.CharField(required=False, widget=forms.TextInput(
            attrs={
                'readonly': 'true',
                'value':'non-checked',
                'display': 'none',
                'style': ' opacity: 0;display:none;'

            }))
    #recieve_newsletter = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


           # }))
    #postal_code = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = MyUser
        fields = ('email', 'password1', 'password2',)


class AgencyForm(UserCreationForm):

    #postal_code = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Agency
        fields = ('package', 'address', 'address1','description','phone','email','website',)



class CountrieForm(forms.ModelForm):

    class Meta:
        model = Countrie
        fields = ('country_name',)

class ProfileAgencyForm(forms.Form):
    myfile = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'visibility': 'hidden',
        'position': 'absolute',
        'top': '-9999px',
        'left': '-9999px',
        'onchange': 'showImage()',
        'data-show-upload': 'false',
        'data-show-caption': 'false',
        'data-show-remove': 'false',
        'data-browse-class': 'btn btn-default',
        'data-browse-label': 'Browse Images',

        'accept': 'image/jpeg,image/png',

    }))

    Agency_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Address_Line_1 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Address_Line_2 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    City = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Phone = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Website = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    bio = forms.CharField(
        required=False,
        max_length=2000
        , widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4'

            })
    )
    skype = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    twitter = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    facebook = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    Pintrest = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    def clean(self):
        cleaned_data = super(ProfileAgencyForm, self).clean()
        name = cleaned_data.get('Agency_Name')
        email = cleaned_data.get('Email')
        message = cleaned_data.get('Phone')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['Your_Agency'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Agencie.objects.all()]
        )


    First_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Last_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Phone = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    bio = forms.CharField(
        required=False,
        max_length=2000
        , widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4'

            })
    )
    skype = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    twitter = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    facebook = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    Pintrest = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        name = cleaned_data.get('Your_Name')
        email = cleaned_data.get('Email')
        message = cleaned_data.get('Phone')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

class ProfileOrdForm(forms.Form):

    First_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Last_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Phone = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))

    skype = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    twitter = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    facebook = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    Pintrest = forms.CharField(required=False,max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))

    def clean(self):
        cleaned_data = super(ProfileOrdForm, self).clean()
        name = cleaned_data.get('Your_Name')
        email = cleaned_data.get('Email')
        message = cleaned_data.get('Phone')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')



class SendmessageForm(forms.Form):

    Your_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    Your_Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    Your_Message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',

        }),

    )

class ratingForm(forms.Form):

    Your_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly':'true',

        }))
    Your_Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'true',

        }))
    Your_Comment = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',

        }),

    )

class nonratingForm(forms.Form):

    Your_Name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    Your_Email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    Your_Comment = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',

        }),

    )


class ContactForm(forms.Form):
    choice = ["a","b","c"]
    #js.index()
    Your_choice = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )
    Your_Name = forms.CharField(max_length=30 ,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    Your_Email = forms.EmailField(max_length=254,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    Your_Message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
                'class':'form-control',

            }),

    )



    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


class SearchForm(forms.Form):
    choice = ["City","Lusaka" ,"Ndola" ,"Kitwe" ,"Kabwe" ,"Chingola" ,"Mufulira"	,"Livingstone","Luanshya" ,"Kasama","Chipata"]
    #js.index()
    city = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )

    choice = ["status","sale", "rent"]
    # js.index()
    status = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )

    choiceprop = ["Type","Apartment", "Cottage", "Condonium", "Cottage", "Flat", "House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )

    choize = ["Towns","Chadiza","Chama","Chambeshi","Chavuma","Chembe","Chibombo","Chiengi","Chilubi","Chinsali","Chinyingi","Chirundu","Chisamba","Choma","Gwembe","Isoka","Kabompo","Kafue","Kafulwe","Kalabo","Kalene Hill","Kalomo","Kalulushi","Kanyembo","Kaoma","Kapiri Mposhi","Kasempa","Kashikishi","Kataba","Katete","Kawambwa","Kazembe","Kazungula","Kibombomene","Luangwa","Lufwanyama","Lukulu","Lundazi","Macha Mission","Makeni""Maliti","Mansa","Mazabuka","Mbala","Mbereshi","Mfuwe","Milenge","Misisi","Mkushi","Mongu","Monze","Mpika","Mporokoso","Mpulungu","Mumbwa","Muyombe","Mwinilunga","Nchelenge","Ngoma","Nkana","Nseluka","Pemba","Petauke","Samfya","Senanga","Serenje","Sesheke","Shiwa Ngandu","Siavonga","Sikalongo","Sinazongwe","Zambezi","Zimba"]
    town = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )

    choize = ["provinces","Copperbelt","Luapula","Muchinga","North-Western","Western","Southern","Central","Lusaka","Eastern","Northern"]
    provinces = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )

    price_range = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name' : 'price',
           'value' : '1000;2990000',

        }))


    def clean(self):
        cleaned_data = super(SearchForm, self).clean()



class AgencyCreate(forms.Form):
    Agent_name = forms.CharField(max_length=30 ,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    address_line_1 = forms.CharField(max_length=255, widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    address_line_2 = forms.CharField(max_length=255, widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    phone = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255, widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    website = forms.CharField(max_length=255, widget=forms.TextInput(  attrs={
                'class':'form-control',

            }))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    description = forms.CharField(
        max_length=2000
    , widget = forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows':'4'

        })
    )

    package = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'true',
            'visibility': 'hidden',

        }))


    def clean(self):
        cleaned_data = super(AgencyCreate, self).clean()
        name = cleaned_data.get('Agent_name')
        email = cleaned_data.get('address_line_1')
        description = cleaned_data.get('address_line_2')
        if not name and not email and not description:
            raise forms.ValidationError('This fiels is required!')

class PropCreate(forms.Form):
    choiceprop = ["Property Type", "Apartment", "Cottage", "Condonium", "Cottage", "Flat", "House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )

    choize = ["Towns", "Chadiza", "Chama", "Chambeshi", "Chavuma", "Chembe", "Chibombo", "Chiengi", "Chilubi",
              "Chinsali", "Chinyingi", "Chirundu", "Chisamba", "Choma", "Gwembe", "Isoka", "Kabompo", "Kafue",
              "Kafulwe", "Kalabo", "Kalene Hill", "Kalomo", "Kalulushi", "Kanyembo", "Kaoma", "Kapiri Mposhi",
              "Kasempa", "Kashikishi", "Kataba", "Katete", "Kawambwa", "Kazembe", "Kazungula", "Kibombomene", "Luangwa",
              "Lufwanyama", "Lukulu", "Lundazi", "Macha Mission", "Makeni""Maliti", "Mansa", "Mazabuka", "Mbala",
              "Mbereshi", "Mfuwe", "Milenge", "Misisi", "Mkushi", "Mongu", "Monze", "Mpika", "Mporokoso", "Mpulungu",
              "Mumbwa", "Muyombe", "Mwinilunga", "Nchelenge", "Ngoma", "Nkana", "Nseluka", "Pemba", "Petauke", "Samfya",
              "Senanga", "Serenje", "Sesheke", "Shiwa Ngandu", "Siavonga", "Sikalongo", "Sinazongwe", "Zambezi",
              "Zimba"]
    town = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )

    choize = ["provinces", "Copperbelt", "Luapula", "Muchinga", "North-Western", "Western", "Southern", "Central",
              "Lusaka", "Eastern", "Northern"]
    provinces = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )
    choice = ["City", "Lusaka", "Ndola", "Kitwe", "Kabwe", "Chingola", "Mufulira", "Livingstone", "Luanshya", "Kasama",
              "Chipata"]
    # js.index()
    city = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'visibility': 'hidden',
        'position': 'absolute',
        'top': '-9999px',
        'left': '-9999px',
        'onchange':'showImage()',
        'data-show-upload': 'false',
        'data-show-caption': 'false',
        'data-show-remove': 'false',
        'data-browse-class': 'btn btn-default',
        'data-browse-label': 'Browse Images',

        'accept': 'image/jpeg,image/png',

    }))

    title = forms.CharField(max_length=30 ,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
                'class':'form-control',

            }))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    baths = forms.IntegerField()
    beds = forms.IntegerField()
    area = forms.IntegerField()
    garages = forms.IntegerField(required=False)





    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
                'class':'form-control',


            }),

    )


    choice = ["sale", "rent"]
    # js.index()
    status = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )
    choice = ["Cash", "Debit"]
    # js.index()
    payment_option = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )

    choiceprop = ["Apartment", "Cottage","Condonium","Cottage","Flat","House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )
    CHOICES = (
        ("True", "True"),
        ("False", "False"),

    )
    Allow_User_rating = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style': 'position: absolute; opacity: 0;'

    }))

    Air_conditioning = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    bedding = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    heating = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    garrage = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Toaster = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Parquet = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Beach = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Garrage = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Cable_TV = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    pool = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Balcony = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Hi_Fi = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Bedding = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Microwave = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Toaster = forms.ChoiceField(choices=CHOICES,required=False, widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Balcony = forms.ChoiceField(choices=CHOICES,required=False, widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Smoking_allowed = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Coffee_pot = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Roof_terrace = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    iron = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))






    def clean(self):
        cleaned_data = super(PropCreate, self).clean()
        name = cleaned_data.get('title')
        email = cleaned_data.get('price')
        message = cleaned_data.get('baths')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
class PropEdit(forms.Form):
    choiceprop = ["Property Type", "Apartment", "Cottage", "Condonium", "Cottage", "Flat", "House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )

    choize = ["Towns", "Chadiza", "Chama", "Chambeshi", "Chavuma", "Chembe", "Chibombo", "Chiengi", "Chilubi",
              "Chinsali", "Chinyingi", "Chirundu", "Chisamba", "Choma", "Gwembe", "Isoka", "Kabompo", "Kafue",
              "Kafulwe", "Kalabo", "Kalene Hill", "Kalomo", "Kalulushi", "Kanyembo", "Kaoma", "Kapiri Mposhi",
              "Kasempa", "Kashikishi", "Kataba", "Katete", "Kawambwa", "Kazembe", "Kazungula", "Kibombomene", "Luangwa",
              "Lufwanyama", "Lukulu", "Lundazi", "Macha Mission", "Makeni""Maliti", "Mansa", "Mazabuka", "Mbala",
              "Mbereshi", "Mfuwe", "Milenge", "Misisi", "Mkushi", "Mongu", "Monze", "Mpika", "Mporokoso", "Mpulungu",
              "Mumbwa", "Muyombe", "Mwinilunga", "Nchelenge", "Ngoma", "Nkana", "Nseluka", "Pemba", "Petauke", "Samfya",
              "Senanga", "Serenje", "Sesheke", "Shiwa Ngandu", "Siavonga", "Sikalongo", "Sinazongwe", "Zambezi",
              "Zimba"]
    town = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )

    choize = ["provinces", "Copperbelt", "Luapula", "Muchinga", "North-Western", "Western", "Southern", "Central",
              "Lusaka", "Eastern", "Northern"]
    provinces = forms.ChoiceField(
        choices=[(o, str(o)) for o in choize]
    )
    choice = ["City", "Lusaka", "Ndola", "Kitwe", "Kabwe", "Chingola", "Mufulira", "Livingstone", "Luanshya", "Kasama",
              "Chipata"]
    # js.index()
    city = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )
    #prop_id = forms.IntegerField(widget=forms.NumberInput())
    video = forms.CharField (required=False,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    myfile = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'visibility': 'hidden',
        'position': 'absolute',
        'top': '-9999px',
        'left': '-9999px',
        'onchange':'showImage()',
        'data-show-upload': 'false',
        'data-show-caption': 'false',
        'data-show-remove': 'false',
        'data-browse-class': 'btn btn-default',
        'data-browse-label': 'Browse Images',

        'accept': 'image/jpeg,image/png',

    }))

    title = forms.CharField(max_length=30 ,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
                'class':'form-control',

            }))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control',

        }))
    baths = forms.IntegerField()
    beds = forms.IntegerField()
    area = forms.IntegerField()
    garages = forms.IntegerField(required=False)





    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
                'class':'form-control',


            }),

    )

    tags = forms.CharField(
        required=False,
        max_length=2000
        , widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '2',
                'onkeyup':'tag()',

            })
    )


    choice = ["sale", "rent"]
    # js.index()
    status = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )
    choice = ["Cash", "Debit"]
    # js.index()
    payment_option = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )

    choiceprop = ["Apartment", "Cottage","Condonium","Cottage","Flat","House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )
    CHOICES = (
        ("True", "True"),
        ("False", "False"),

    )
    Allow_User_rating = forms.ChoiceField(choices=CHOICES,required=False,widget=forms.CheckboxInput(attrs={
        #'style': 'position: absolute; opacity: 0;'

    }))








    def clean(self):
        cleaned_data = super(PropEdit, self).clean()
        name = cleaned_data.get('title')
        email = cleaned_data.get('price')
        message = cleaned_data.get('baths')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

class PropertyCreate(forms.Form):
    title = forms.CharField(max_length=30 ,widget=forms.TextInput(
            attrs={
                'class':'form-control',

            }))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
                'class':'form-control',

            }))
    baths = forms.IntegerField()
    beds = forms.IntegerField()
    area = forms.IntegerField()
    garages = forms.IntegerField(required=False)
    latitude = forms.IntegerField(required=False,widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'readonly':'true',


            }))
    longitude = forms.IntegerField(required=False ,widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'readonly':'true',
                'visibility': 'hidden',

            }))
    package = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'true',
            'visibility': 'hidden',

        }))




    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
                'class':'form-control',


            }),

    )
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={
                'class':'file',
        'multiple':'true',
        'data-show-upload':'false',
        'data-show-caption':'false',
        'data-show-remove': 'false',
        'data-browse-class': 'btn btn-default',
        'data-browse-label': 'Browse Images',

        'accept':'image/jpeg,image/png',



            }))

    choice = ["sale", "rent"]
    # js.index()
    status = forms.ChoiceField(
        choices=[(o, str(o)) for o in choice]
    )

    choiceprop = ["Apartment", "Cottage","Condonium","Cottage","Flat","House"]
    Property_type = forms.ChoiceField(
        choices=[(o, str(o)) for o in choiceprop]
    )
    Allow_User_rating = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style': 'position: absolute; opacity: 0;'

    }))

    Air_conditioning = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    bedding = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    heating = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    garrage = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Toaster = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Parquet = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Beach = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Garrage = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Cable_TV = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    pool = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Balcony = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Hi_Fi = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Bedding = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Microwave = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Toaster = forms.ChoiceField(required=False, widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Balcony = forms.ChoiceField(required=False, widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Smoking_allowed = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Coffee_pot = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    Roof_terrace = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))
    iron = forms.ChoiceField(required=False,widget=forms.CheckboxInput(attrs={
        #'style' :'position: absolute; opacity: 0;'


            }))






    def clean(self):
        cleaned_data = super(PropertyCreate, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('description')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')