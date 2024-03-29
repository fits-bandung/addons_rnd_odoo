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
    'website': "https://fujicon-japan.com/",
    'images': ['images/tax.png'],
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['hr','hr_payroll','hr_contract'],
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
    'demo': [
        'demo/demo.xml',
    ],
}
