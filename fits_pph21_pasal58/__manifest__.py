# -*- coding: utf-8 -*-
{
    'name': "Indonesia Tax Pph 21 pasal 58 Computation on Payslip",
    'summary': """
        Perhitungan Pph 21 Pasal 58 dengan menggunakan Tabel TER (Tarif Efektif Rata - Rata) Kategori.
       """,
    'description': """
       Addons ini menambahkan fungsionalitas Pajak Penghasilan (PPh) Pasal 21 Pasal 58 pada Odoo. 
       Dengan addon ini, kita dapat mengelola PPh 21 secara efisien untuk karyawan yang menerima 
       penghasilan berdasarkan ketentuan Pasal 58 UU PPh.
    """,
    'author': "PT Fujicon Priangan Perdana",
    'sequence': -100,
    'website': "https://fujicon-japan.com/",
    'images': ['images/fpp.gif'],
    'category': 'Human Resources',
    'version': '17.0.1.0.0',
    'price': 300.00,
    'currency': 'USD',
    'license': 'AGPL-3',
    'depends': ['hr', 'om_hr_payroll', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/payslip_kategori_ter_view.xml',
        'views/inherit_hr_payslip_view.xml',
        'views/inherit_hr_employee_view.xml',
        'views/inherit_hr_contract_view.xml',
        'data/data_salary.xml',
        'data/data_pph21_ter_a_gross.xml',
        'data/data_pph21_ter_b_gross.xml',
        'data/data_pph21_ter_c_gross.xml',
        'data/data_pph21_ter_a_grossup.xml',
        'data/data_pph21_ter_b_grossup.xml',
        'data/data_pph21_ter_c_grossup.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
