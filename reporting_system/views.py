from django.shortcuts import render, redirect
from reporting_system.forms.correction_report_form import CorrectionReportForm
from reporting_system.forms.document_form import DocumentForm
from reporting_system.models.correction_report import CorrectionReport


def index(request):
    return render(request, 'cms/index.html')


def add_correction_report(request):
    if request.method == 'POST':
        form = CorrectionReportForm(request.POST)
        auction = CorrectionReport()
        # if form.is_valid():
        #     return redirect('show_auction', auction.id) \
        #         if AuctionsService.add_auction(request, auction=auction, form=form) \
        #         else redirect('add_auction')
        # else:
        #     return redirect('add_auction')
    else:
        return render(request, 'forms/add_correction_report.html', {
            'page_title': 'Neue Korrekturmeldung',
            'header': 'Eine neue Korrekturmeldung erstellen',
            'form': CorrectionReportForm(),
            'document_form': DocumentForm(),
        })
