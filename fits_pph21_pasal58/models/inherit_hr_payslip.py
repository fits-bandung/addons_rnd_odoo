from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _


class HRPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    is_tahunan = fields.Boolean(string='Payslip Tahunan', default=False)

class HRPayslip(models.Model):
    _inherit = 'hr.payslip'

    pendapatan_bruto_tahunan = fields.Float(string="Bruto Tahunan", readonly=True)
    pendapatan_bruto_bulanan = fields.Float(string='Bruto Bulanan', readonly=True)
    pph21_bulanan = fields.Float(string="Pph21 Bulanan", readonly=True)
    pph21_tahunan = fields.Float(string="Pph21 Tahunan", readonly=True)
    is_tahunan = fields.Boolean(string="Payslip Tahunan", related='payslip_run_id.is_tahunan', readonly=False, store=True)
    tunjangan_pajak = fields.Selection([('gross', 'Gross'), ('grossup', 'GrossUp')], related='contract_id.tunjangan_pajak', readonly=False, string="Metode Pajak", required=True)
    bruto_pph_ids = fields.One2many('hr.payslip.line.bruto.pph', 'payslip_id', string='Payslip')

    def delete_generate_payslip_lines_bruto_pph(self):
        for payslip in self:
            existing_lines = self.env['hr.payslip.line.bruto.pph'].search([
                    ('payslip_id', '=', payslip.id),
                ])
            existing_lines.sudo().unlink()

    def generate_payslip_lines_bruto_pph(self):
        for payslip in self:
            date = fields.Date.from_string(self.date_from)
            start_date = (date).strftime('%Y-01-01')
            end_date = fields.Date.from_string(start_date)
            date_end = (end_date + relativedelta(months=+12, day=1, days=-1)).strftime('%Y-%m-%d')

            # Delete existing hr.payslip.line.bruto.pph records if is_tahunan is False


            payslip_filter = self.env['hr.payslip'].search(
                [('employee_id', '=', payslip.employee_id.id),('state', '=', 'done'),('date_from', '>=', start_date),
                 ('date_from', '<=', date_end)])
            payslip_filter_draft = self.env['hr.payslip'].search(
                [('employee_id', '=', payslip.employee_id.id), ('state', '=', 'draft'), ('date_from', '>=', start_date),
                 ('date_from', '<=', date_end)])



            # Proses data dan buat entri di hr.payslip.line
            for line_data in payslip_filter:  # Gantilah ini dengan metode sesuai kebutuhan Anda
                existing_line = self.env['hr.payslip.line.bruto.pph'].search([
                    ('payslip_id', '=', payslip.id),
                    ('ref', '=', line_data.number),
                    # Tambahkan kriteria tambahan jika diperlukan
                ])
                if not existing_line:
                    payslip_line_vals = {
                        'payslip_id': payslip.id,
                        'ref': line_data.number,
                        'payslip_name': line_data.name,
                        'date_from': line_data.date_from,
                        'date_to': line_data.date_to,
                        'bruto_bulanan': line_data.pendapatan_bruto_bulanan,
                        'pph21_bulanan': line_data.pph21_bulanan,
                        'status': line_data.state
                    }
                    self.env['hr.payslip.line.bruto.pph'].create(payslip_line_vals)

            for line_data in payslip_filter_draft:
                existing_line = self.env['hr.payslip.line.bruto.pph'].search([
                    ('payslip_id', '=', payslip.id),
                    ('ref', '=', line_data.number),
                    # Tambahkan kriteria tambahan jika diperlukan
                ])
                if not existing_line:
                    payslip_line_vals = {
                        'payslip_id': payslip.id,
                        'ref': line_data.number,
                        'payslip_name': line_data.name,
                        'date_from': line_data.date_from,
                        'date_to': line_data.date_to,
                        'bruto_bulanan': line_data.pendapatan_bruto_bulanan,
                        'pph21_bulanan': 0,
                        'status': line_data.state
                    }
                    self.env['hr.payslip.line.bruto.pph'].create(payslip_line_vals)

    def _compute_pendapatan_bruto(self):
        for payslip in self:
            gross_amount = sum(line.amount for line in payslip.line_ids if line.category_id.code == 'GrossPph')
            payslip.pendapatan_bruto_bulanan = gross_amount


            if payslip.tunjangan_pajak == "gross":
                metode_payslip = self.env['payslip.kategori.ter'].search([('tunjangan_pajak', '=', 'gross'),('status_sipil_ter_ids.status_sipil', '=', payslip.employee_id.status_sipil)], limit=1)
                if metode_payslip:
                    get_ter = self.env['payslip.line.kategori.ter'].search([
                            ('kategori_ter_id', '=', metode_payslip.id),
                            ('bruto_bulanan_awal', '<=', payslip.pendapatan_bruto_bulanan),
                            ('bruto_bulanan_akhir', '>=', payslip.pendapatan_bruto_bulanan)
                        ], limit=1)
                    if get_ter :
                            payslip.pph21_bulanan = payslip.pendapatan_bruto_bulanan * get_ter.persentase_nilai

                    else :
                        payslip.pph21_bulanan = 0
            else :
                metode_payslip = self.env['payslip.kategori.ter'].search([('tunjangan_pajak', '=', 'grossup'),('status_sipil_ter_ids.status_sipil', '=', payslip.employee_id.status_sipil)], limit=1)
                if metode_payslip:
                    get_ter = self.env['payslip.line.kategori.ter'].search([
                            ('kategori_ter_id', '=', metode_payslip.id),
                            ('bruto_bulanan_awal', '<=', payslip.pendapatan_bruto_bulanan),
                            ('bruto_bulanan_akhir', '>=', payslip.pendapatan_bruto_bulanan)
                        ], limit=1)
                    if get_ter:
                            payslip.pph21_bulanan = (payslip.pendapatan_bruto_bulanan * get_ter.persentase_nilai) / (1 - get_ter.persentase_nilai)

                    else:
                        payslip.pph21_bulanan = 0

    def get_bruto_tahunan(self):
        for x in self:
            date = fields.Date.from_string(self.date_from)
            start_date = (date).strftime('%Y-01-01')
            end_date = fields.Date.from_string(start_date)
            date_end = (end_date + relativedelta(months=+12, day=1, days=-1)).strftime('%Y-%m-%d')
            print('==================date===============', start_date, date_end)
            bruto_tahunan = self.env['hr.payslip'].search([('employee_id', '=', x.employee_id.id),('state', '=', 'done'),('date_from', '>=', start_date),('date_from', '<=', date_end)])
            print('===================payslip=================', bruto_tahunan)
            sum_bruto_tahunan = 0
            for bt in bruto_tahunan:
                sum_bruto_tahunan += bt.pendapatan_bruto_bulanan
                x.pendapatan_bruto_tahunan = sum_bruto_tahunan + x.pendapatan_bruto_bulanan

    def get_pph_tahunan(self):
        for x in self:
            date = fields.Date.from_string(self.date_from)
            start_date = (date).strftime('%Y-01-01')
            end_date = fields.Date.from_string(start_date)
            date_end = (end_date + relativedelta(months=+11, day=1, days=-1)).strftime('%Y-%m-%d')
            print('==================date===============', start_date, date_end)
            pph_tahunan = self.env['hr.payslip'].search([('employee_id', '=', x.employee_id.id),('state', '=', 'done'),('date_from', '>=', start_date),('date_from', '<=', date_end)])
            print('===================payslip=================', pph_tahunan)
            sum_bruto_tahunan = 0
            for pph in pph_tahunan:
                sum_bruto_tahunan += pph.pph21_bulanan
                x.pph21_tahunan = sum_bruto_tahunan




    @api.multi
    def compute_sheet(self):
        # Call the original compute_sheet method from the parent class
        super(HRPayslip, self).compute_sheet()

        # Add your custom logic here
        for payslip in self:
            payslip._compute_pendapatan_bruto()
            if payslip.is_tahunan == True :
                payslip.get_bruto_tahunan()
                payslip.get_pph_tahunan()
                payslip.generate_payslip_lines_bruto_pph()
            else :
                payslip.pendapatan_bruto_tahunan = 0
                payslip.pph21_tahunan = 0
                payslip.delete_generate_payslip_lines_bruto_pph()
            # Call compute_sheet again after your custom logic
        super(HRPayslip, self).compute_sheet()

        return True




class HRPayslipLinesBrutoPph(models.Model):
    _name = 'hr.payslip.line.bruto.pph'

    payslip_id = fields.Many2one('hr.payslip',string="Payslip ID")
    ref = fields.Char(string="Reference", readonly=True)
    date_from = fields.Char(string="Date From", readonly=True)
    date_to = fields.Char(string="Date To ", readonly=True)
    payslip_name = fields.Char(string="Payslip Name", readonly=True)
    bruto_bulanan = fields.Float(string='Bruto Bulanan', readonly=True)
    pph21_bulanan = fields.Float(string="Pph21 Bulanan", readonly=True)
    status = fields.Char(string="Status", readonly=True)


