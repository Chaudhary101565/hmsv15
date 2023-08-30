from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import phonenumbers


class PhoneCalls(models.Model):
    _name = 'phone.calls'
    _description = 'Phone Calls'
    _order = 'id desc'
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True, readonly=True, default=lambda self: _('New'))
    caller_phone = fields.Char(string='Caller Phone', tracking=True)
    call_start_time = fields.Datetime(string='Call Start Time', tracking=True)
    call_end_time = fields.Datetime(string='Call End Time', tracking=True)

    @api.model
    def create(self, vals):
        """Used to Create sequence and call phone number formatted method if caller phone is enter"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'phone.calls') or _('New')
        if 'caller_phone' in vals:
            phone_number = vals.get('caller_phone')
            if phone_number:
                formatted_phone = self.phone_number_format(phone_number)
                vals['caller_phone'] = formatted_phone
        res = super(PhoneCalls, self).create(vals)
        return res

    def write(self, vals):
        """if changes are made in the caller_phone field then phone number format method call"""
        if 'caller_phone' in vals:
            phone_number = vals.get('caller_phone')
            if phone_number:
                formatted_phone = self.phone_number_format(phone_number)
                vals['caller_phone'] = formatted_phone
        return super(PhoneCalls, self).write(vals)

    def phone_number_format(self, phone_number):
        """return formatted phone number"""
        if phone_number.isdigit() and len(phone_number) == 10:
            default_region = 'IN'
            parsed_phone = phonenumbers.parse(phone_number, default_region)
            formatted_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return formatted_phone
        raise ValidationError(_('Please enter valid phone number.'))

    @api.constrains('call_start_time', 'call_end_time')
    def validate_call_start_end_time(self):
        """Method to validate Call Start And End Time"""
        if self.call_end_time < self.call_start_time:
            raise ValidationError(_('Call end time cannot be earlier than call start time'))
