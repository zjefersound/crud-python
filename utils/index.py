def formatar_moeda(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return "R$ "+c.replace('v','.')