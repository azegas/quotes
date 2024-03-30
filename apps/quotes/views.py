from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from apps.quotes.models import Quote
from apps.quotes.forms import QuoteForm
from ag_mixins import AgObjectRetrievalMixin


class QuoteListView(View):
    '''
    gCVB example:
    
    class QuoteListView(ListView):
        model = Quote
        template_name = "quotes/quote_list.html" # default
    '''

    template_name = 'quotes/quote_list.html'

    def get(self, request):
        quotes = Quote.objects.all()
        return render(request, self.template_name, {'object_list' : quotes})


class QuoteDetailView(AgObjectRetrievalMixin, View):
    '''
    gCVB example:

    class QuoteDetailView(DetailView):
        model = Quote
        template_name = "quotes/quote_detail.html" # default
    '''

    template_name = 'quotes/quote_detail.html'
    
    def get(self, request, pk):
        quote = self.ag_get_object_by_id(Quote, pk)
        return render(request, self.template_name, {'quote' : quote})
    

class QuoteCreateView(View):
    '''
    gCVB example:
    
    class QuoteCreateView(CreateView):
        model = Quote
        fields = ["text", "author", "active",]
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_form.html" # default
    '''

    form_class = QuoteForm
    template_name = "quotes/quote_form.html"
    success_url = reverse_lazy('quote-list')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request):
        '''
        The post method handles form submission

        1. It creates a form instance populated with request.POST data 
        2. checks if the form is valid
        3. saves the form if so
        '''

        form = self.form_class(request.POST)

        if form.is_valid():
            # form.save() # would use this if it was a forms.ModelForm
            text = form.cleaned_data['text']
            author = form.cleaned_data['author']
            active = form.cleaned_data['active']
            quote = Quote.objects.create(text=text, author=author, active=active)
            quote.save()
            return HttpResponseRedirect(self.success_url)
        else:
            form = QuoteForm()
        
        return render(request, self.template_name, {'form' : form})


class QuoteDeleteView(AgObjectRetrievalMixin, View):
    '''
    class QuoteDeleteView(DeleteView):
        model = Quote
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_confirm_delete.html" # default
    '''

    template_name = "quotes/quote_confirm_delete.html"
    success_url = reverse_lazy('quote-list')

    def get(self, request, pk):
        quote = self.ag_get_object_by_id(Quote, pk)
        return render(request, self.template_name, {'object' : quote})
    
    def post(self, request, pk):
        quote = self.ag_get_object_by_id(Quote, pk)
        quote.delete()
        return HttpResponseRedirect(self.success_url)


class QuoteUpdateView(AgObjectRetrievalMixin, View):
    '''
    class QuoteUpdateView(UpdateView):
        model = Quote
        fields = "__all__"
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_form.html" # default
    '''

    form_class = QuoteForm
    template_name = "quotes/quote_form.html"
    success_url = reverse_lazy('quote-list')

    def get(self, request, pk):
        quote = self.ag_get_object_by_id(Quote, pk)
        form = self.form_class(
            initial={
                'text' : quote.text,
                'author' : quote.author,
                'active' : quote.active,
            }
        )
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request, pk):
        quote = self.ag_get_object_by_id(Quote, pk)
        form = self.form_class(request.POST)

        if form.is_valid():
            quote.text = form.cleaned_data['text']
            quote.author = form.cleaned_data['author']
            quote.active = form.cleaned_data['active']
            quote.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})