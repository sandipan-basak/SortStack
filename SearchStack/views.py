import requests
import pytz
from datetime import datetime
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth import login
# from django.core.cache import cache
# from django.core.cache.utils import make_template_fragment_key
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from .models import User, Article, Folder, ArticleList
from .forms import UserSignUpForm, SearchForm

# Create your views here.
def home(request):
    print(request.user)
    print("at home")
    if request.user.is_authenticated:
        return redirect('search:query')
    return render(request, 'home.html')

class UserSignUp(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        user.set_password(self.request.POST.get('password'))
        user.save()
        login(self.request, user)
        return redirect('search:query')

@method_decorator([login_required,], name='dispatch')
class FolderListView(ListView):
    model = Folder
    template_name = 'folder_view.html'
    pass
@method_decorator([login_required,], name='dispatch')
class Folder(DetailView):
    model = Folder
    pass

def session_check(request, context):
    now = datetime.now()
    if 'short' in request.session or 'long' in request.session:
        diffs = (now - datetime.fromtimestamp(request.session['short'])).seconds
        diffl = (now - datetime.fromtimestamp(request.session['long'])).seconds
        if (request.session['shortq'] == 5 and diffs <= 60) or (request.session['longq'] == 100 and diffl <= 24*60*60):
            context['limit'] = True
            print(context['limit'])
        elif diffs > 60 and request.session['shortq'] <= 5:
            request.session['shortq'] = 0
            request.session['short'] = datetime.timestamp(now)
            context['limit'] = False
        elif diffs > 24*60*60 and request.session['longq'] <= 100:
            request.session['longq'] = 0
            request.session['long'] = datetime.timestamp(now)
            context['limit'] = False
    else:
        if 'short' not in request.session:
            request.session['short'] = datetime.timestamp(datetime.now())
        if 'long' not in request.session:
            request.session['long'] = datetime.timestamp(datetime.now())    

@login_required
def query_article(request):
    articles = None
    form = SearchForm()
    context = {
        'form': form,
        'None': None,
        'limit': False
    }
    if request.method == 'POST':
        if 'search_query' in request.POST:
            session_check(request, context)
            if not context['limit']:
                request.session['shortq'] = request.session['shortq'] + 1 if 'shortq' in request.session else 1
                request.session['longq'] = request.session['longq'] + 1 if 'longq' in request.session else 1
                print(request.session['shortq'])
                print(request.session['longq'])
                ArticleList.objects.all().delete()
                data = request.POST
                re_data = {}
                for key, value in request.POST.items():
                    if key == 'search_query' or key == 'csrfmiddlewaretoken':
                        continue
                    if value != '':
                        re_data[key] = value
                re_data['site'] = 'stackoverflow'
                re_data['filter'] = '!nMp.SvPX.C'
                re_data['pagesize'] = '100' if 'pagesize' not in re_data else re_data['pagesize']
                re_data['q'] = re_data.pop('query')
                lookup_url = f"{'https://api.stackexchange.com/2.2/search/advanced'}?{urlencode(re_data)}"
                rejson = requests.get(lookup_url).json()
                # key = make_template_fragment_key('artcile_view', [request.user.username])
                articles = []
                content = {}
                for sub in rejson['items']:
                    ArticleList.objects.create(title=sub['title'],
                                               view_count=sub['view_count'],
                                               link=sub['link'], 
                                               creation_date=(datetime.fromtimestamp(int(sub['creation_date']))).replace(tzinfo=pytz.UTC))
                return redirect('search:set')
    return render(request, 'search.html', context=context)

@method_decorator([login_required,], name='dispatch')
class ArticleSetView(ListView):
    model = ArticleList
    counts = ArticleList.objects.count()
    context_object_name = 'articles'
    paginate_by = 10 if counts > 10 else counts
    template_name = 'articles.html'

    def get_queryset(self):
        return ArticleList.objects.all()


     