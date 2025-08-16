from django.shortcuts import render
from section2.classes import Naturals

# Create your views here.
def display_section_2(request, num_to_extract=None):
    natural_nums = Naturals()
    message = ''
    DEFAULT_NUM_TO_EXTRACT = 55

    if num_to_extract is not None:
        if natural_nums.is_valid_to_extract(num_to_extract):
            natural_nums.extract(num_to_extract)
        else:
            message = f'El valor { num_to_extract } no es válido'
    else:
        natural_nums.extract(DEFAULT_NUM_TO_EXTRACT)
        message = f'Se utiliza el valor por default para la prueba: { DEFAULT_NUM_TO_EXTRACT }'

    return render(request,
                  'display_section2.html',
                  {
                      "html_table": natural_nums.get_lost(),
                      "list_naturals": natural_nums._get_num_list(),
                      "message": message,
                   })