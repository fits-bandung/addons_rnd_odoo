from odoo import models, fields, api


class PayslipKategoriTer(models.Model):
    _name = 'payslip.kategori.ter'
    _description = 'Payslip Kategori TER'
    _rec_name = 'nama'

    nama = fields.Char(string="Nama")
    tunjangan_pajak = fields.Selection([('gross', 'Gross'), ('grossup', 'GrossUp')], string="Metode Pajak")
    kategori_ter_ids = fields.One2many('payslip.line.kategori.ter', 'kategori_ter_id', string="Kategori TER IDS")
    status_sipil_ter_ids = fields.One2many('payslip.line.status.sipil', 'status_sipil_ter_id', string="Status Sipil TER IDS")
class PayslipLineStatusSipilTer(models.Model):
    _name = 'payslip.line.status.sipil'
    _description = 'Payslip Line Status Sipil'

    status_sipil_ter_id = fields.Many2one('payslip.kategori.ter', string="Status Sipil TER Id")
    status_sipil = fields.Selection([('TK/0', 'TK/0'),('TK/1', 'TK/1'),
                                      ('TK/2', 'TK/2'),('TK/3', 'TK/3'),
                                      ('K/0', 'K/0'),('K/1', 'K/1'),
                                      ('K/2', 'K/2'),('K/3', 'K/3')], string="Status Sipil")

class PayslipLineKategoriTer(models.Model):
    _name = 'payslip.line.kategori.ter'
    _description = 'Payslip Line Kategori TER'

    kategori_ter_id = fields.Many2one('payslip.kategori.ter', string="Kategori TER Id")
    bruto_bulanan_awal = fields.Float(string="Bruto Bulanan Awal")
    bruto_bulanan_akhir = fields.Float(string="Bruto Bulanan Akhir")
    persentase_nilai = fields.Float(string="Persentase Nilai", digits=(12, 4))
