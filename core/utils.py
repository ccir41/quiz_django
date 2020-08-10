from django.contrib.admin.views.decorators import staff_member_required


class StaffMemberRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return staff_member_required(view)
