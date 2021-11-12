from django.shortcuts import render, redirect
from django.views import View
import time
import json
from collections import defaultdict

from .forms import WordForm
from .models import WordList, Pattern
import tk.fitter as ft
import tk.sorter as st


# Create your views here.
class AssembleView(View):
    template_name = 'bot/bot_assemble.html'
    # queryset = WordModel.objects.all()

    def get(self, request, *args, **kwargs):
        print(request.GET)
        words = defaultdict(str)
        words['words_raw'] = request.GET.get('words_raw')
        word_form = WordForm(initial=words)
        context = {
            'form': word_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        word_form = WordForm(request.POST)
        print(request.POST)
        if word_form.is_valid():
            words = word_form.save()
            self.gen_crossword(words)
            # return redirect(f'./{words.id}/')  # non-cache
            return redirect(f'./{words.id}/')  # cache
        context = {
            'form': word_form,
        }
        return render(request, self.template_name, context)

    def gen_crossword(self, words_obj):
        words = words_obj.words_raw.split('\r\n')
        # start = time.time()
        n = len(words) - 1
        st.freq_shuffle(words, 0, n, int(n/2))
        gen = ft.gen_crosswords(words)
        patterns = []
        for i in range(10):
            try:
                cw = next(gen)
                print(f'creating combo {i}')
                pattern = Pattern(
                    words = words_obj,
                    locations = cw.get_loc_str(),
                    dimensions = cw.get_dimension(),
                    cross = cw.get_cross_str(),
                    down = cw.get_down_str(),
                    ordering = cw.get_init_str()
                )
                patterns.append(pattern)
            except:
                break
        Pattern.objects.bulk_create(patterns)
        # print(f'Time to execute CW module: {time.time() - start}')


# Use different URL to navigate different combo
# Query database every time new pattern is displayed
class AssembleDetailView(View):
    template_name = 'bot/bot_assemble_detail.html'

    def get_object(self, id):
        # return Combos.objects.filter(words_id=id)
        return WordList.objects.get(id=id).pattern_set.all()

    def get(self, request, id1, *args, **kwargs):
        words = WordList.objects.get(id=id1)
        qs = self.get_object(id1)
        pattern_list = [ins.unpack() for ins in qs]
        form = WordForm(instance=words)
        context = {
            # 'control': control_form,
            # 'combo': pattern_list[id2],
            # 'idx': id2,
            'form': form,
            'words': words.words_clean,
            'qs': pattern_list,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return redirect(f'../')
