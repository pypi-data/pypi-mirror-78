from decouple import config


IMOPAY_ENV = config("IMOPAY_ENV", default="")
"""Ambiente do Imopay"""


IMOPAY_API_KEY = config("IMOPAY_API_KEY", default="")
"""Chave de autenticação Imopay"""
