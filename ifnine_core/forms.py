from django import forms
from ifnine_core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': "Write Review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']