from django.forms import HiddenInput
from django.forms.utils import flatatt
from django.utils import formats
from django.utils.encoding import force_text
from django.utils.html import format_html

class StatusIconWidget(HiddenInput):
	object_type = None
	availability_status = None
	enabled_status = None
	status_description = None
	
	def _format_value(self, value):
		if self.is_localized:
			return formats.localize_input(value)
		return value
	
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
		if value != '':
			# Only add the 'value' attribute if a value is non-empty.
			final_attrs['value'] = force_text(self._format_value(value))
		return format_html('<input{} />', flatatt(final_attrs))
	

