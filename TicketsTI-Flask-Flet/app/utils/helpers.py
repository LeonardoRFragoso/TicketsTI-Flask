from datetime import timedelta
import re
import humanize
from humanize import i18n

def calculate_sla(start_time, end_time, pause_start=None, resume_time=None):
    """
    Calcula o tempo total de atendimento (SLA), descontando o tempo de pausa, se houver.
    """
    total_time = end_time - start_time
    if pause_start and resume_time:
        total_time -= resume_time - pause_start
    
    return total_time

def format_sla(sla_timedelta):
    """
    Formata um timedelta (duração) em um formato mais legível, usando humanize.
    """
    i18n.activate("pt_BR")
    sla_legivel = humanize.naturaldelta(sla_timedelta)
    i18n.deactivate()
    return sla_legivel

def is_valid_email(email):
    """
    Valida se um e-mail fornecido segue o formato correto usando expressões regulares.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def timedelta_to_hours(td):
    """
    Converte um timedelta em um valor de horas com casas decimais.
    """
    return td.total_seconds() / 3600

def format_timedelta(td):
    """
    Formata um timedelta em horas, minutos e segundos.
    """
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
