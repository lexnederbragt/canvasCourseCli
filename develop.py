import sys
import add_to_module

args = []
args += ['-u', 'https://uio.instructure.com/courses/39661']
args += ['-lt', 'UiO website']
args += ['-lu', 'https://www.uio.no']
args += ['-t','Uke 44 - Kapittel 8: Mutations and DNA']

add_to_module.main(args)

sys.exit

#'-u', 'https://uio.instructure.com/courses/39661', '-lt', 'Oppgave notebook (44.oppgaver.ipynb på JupyterHub)', '-lu', 'https://canvas-lti.jupyterhub.uio.no/hub/lti/launch?custom_next=/hub/user-redirect/notebooks/BIOS1100/uke44/44.oppgaver.ipynb', '-ext', '-t', 'Uke 44 - Kapittel 8: Mutations and DNA']

# python add_to_module.py -u https://uio.instructure.com/courses/39661 -lt "Oppgave notebook (44.oppgaver.ipynb på JupyterHub)" -lu https://canvas-lti.jupyterhub.uio.no/hub/lti/launch?custom_next=/hub/user-redirect/notebooks/BIOS1100/uke44/44.oppgaver.ipynb -ext -t "Uke 44 - Kapittel 8: Mutations and DNA"

# python add_to_module.py -u https://uio.instructure.com/courses/39661 -lt "UiO website" -lu https://www.uio.no -t "Uke 44 - Kapittel 8: Mutations and DNA"

# python add_to_module.py -u https://uio.instructure.com/courses/39661 -lt "UiO website" -lu https://www.uio.no -t "Uke 44 - Kapittel 8: Mutations and DNA" --force
