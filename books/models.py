from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    membership_expiration_date = models.DateField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book} checked out by {self.member}"
