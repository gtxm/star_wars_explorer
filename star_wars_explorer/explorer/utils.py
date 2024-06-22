def compute_selected_fields_after_clicking_field_button(field, fields):
    if field in fields:
        selected_fields = list(set(fields) - {field})  # unselect field
    else:
        selected_fields = fields + [field]  # add selected field
    return ",".join(sorted(selected_fields))
