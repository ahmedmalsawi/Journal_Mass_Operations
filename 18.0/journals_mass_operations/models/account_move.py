from odoo import models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def action_mass_move_to_draft(self):
        """Convert multiple posted journal entries to draft"""
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        moves = self.browse(active_ids)
        posted_moves = moves.filtered(lambda m: m.state == 'posted')
        
        if not posted_moves:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Action Needed',
                    'message': 'No posted entries selected. Please select posted entries to set to draft.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Process in batches to avoid timeouts
        batch_size = 50
        processed = 0
        for i in range(0, len(posted_moves), batch_size):
            batch = posted_moves[i:i + batch_size]
            batch.button_draft()
            processed += len(batch)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Successfully set {processed} entries to draft',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def action_mass_move_to_post(self):
        """Post multiple draft journal entries"""
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        moves = self.browse(active_ids)
        draft_moves = moves.filtered(lambda m: m.state == 'draft')
        
        if not draft_moves:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Action Needed',
                    'message': 'No draft entries selected. Please select draft entries to post.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Process in batches
        batch_size = 30  # Smaller batch for posting as it's more resource intensive
        processed = 0
        for i in range(0, len(draft_moves), batch_size):
            batch = draft_moves[i:i + batch_size]
            batch.action_post()
            processed += len(batch)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Successfully posted {processed} entries',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def action_mass_move_cancel(self):
        """Cancel multiple journal entries"""
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        moves = self.browse(active_ids)
        cancelable_moves = moves.filtered(
            lambda m: m.state in ['draft', 'posted']
        )
        
        if not cancelable_moves:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Action Needed',
                    'message': 'No cancelable entries selected. Only draft or posted entries can be cancelled.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        processed = 0
        for move in cancelable_moves:
            try:
                move.button_cancel()
                processed += 1
            except Exception as e:
                # Continue with other moves if one fails
                continue
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success' if processed > 0 else 'Partial Completion',
                'message': f'Successfully cancelled {processed} out of {len(cancelable_moves)} selected entries',
                'type': 'success' if processed == len(cancelable_moves) else 'warning',
                'sticky': False,
            }
        }

    @api.model
    def action_mass_print_entries(self):
        """Print multiple journal entries"""
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        moves = self.browse(active_ids)
        if not moves:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'No entries selected for printing.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Use the standard report action
        return self.env.ref('account.account_invoices').report_action(moves.ids)

    @api.model
    def get_mass_operation_stats(self):
        """Return statistics for mass operations (can be used in views if needed)"""
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {}
        
        moves = self.browse(active_ids)
        return {
            'draft_count': len(moves.filtered(lambda m: m.state == 'draft')),
            'posted_count': len(moves.filtered(lambda m: m.state == 'posted')),
            'cancel_count': len(moves.filtered(lambda m: m.state == 'cancel')),
            'total_count': len(moves),
        }