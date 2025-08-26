    # def add_note_dialog(self):
    #     """Show dialog to add a note to a contact"""
    #     fields = [
    #         ("First Name", "Enter first name"),
    #         ("Last Name", "Enter last name"),
    #         ("Note", "Enter note text")
    #     ]
        
    #     dialog = InputDialog("Add Note", fields, self)
    #     if dialog.exec():
    #         inputs = dialog.get_inputs()
            
    #         # Validate inputs
    #         if not inputs["First Name"] or not inputs["Last Name"] or not inputs["Note"]:
    #             self.show_message("Error", "All fields are required", QMessageBox.Icon.Warning)
    #             return
            
    #         success, message = self.contact_manager.add_note(
    #             inputs["First Name"],
    #             inputs["Last Name"],
    #             inputs["Note"]
    #         )
            
    #         if success:
    #             self.refresh_table()
    #             self.show_status(message)
    #         else:
    #             self.show_message("Error", message, QMessageBox.Icon.Warning)