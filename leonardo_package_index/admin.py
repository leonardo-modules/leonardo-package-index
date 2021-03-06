from django.contrib import admin

from leonardo_package_index.models import Category, Package, PackageExample, Commit, Version


class PackageExampleInline(admin.TabularInline):
    model = PackageExample


class PackageAdmin(admin.ModelAdmin):

    save_on_top = True
    search_fields = ("title",)
    list_filter = ("category",)
    list_display = ("title", "created", )
    date_hierarchy = "created"
    inlines = [
        PackageExampleInline,
    ]
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category", "pypi_url", "repo_url", "usage", "created_by", "last_modified_by", "show_pypi")
        }),
        ("Pulled data", {
            "classes": ("collapse",),
            "fields": ("repo_description", "repo_watchers", "repo_forks", "commit_list", "pypi_downloads", "participants")
        }),
    )


class CommitAdmin(admin.ModelAdmin):
    list_filter = ("package",)


class VersionLocalAdmin(admin.ModelAdmin):
    search_fields = ("package__title",)


class PackageExampleAdmin(admin.ModelAdmin):

    list_display = ("title", )
    search_fields = ("title",)


admin.site.register(Category)
admin.site.register(Package, PackageAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(Version, VersionLocalAdmin)
admin.site.register(PackageExample, PackageExampleAdmin)
