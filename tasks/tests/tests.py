import pytest
from django.urls import reverse
from tasks.models import Task
from .utils import test_id


@pytest.mark.django_db
@test_id("TC001")
def test_homepage_access(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
@test_id("TC002")
def test_update_task_url(client):
    # Création d’une tâche pour disposer d’un ID valide
    task = Task.objects.create(title="Test task")

    url = reverse("update_task", args=[task.id])
    response = client.get(url)

    # On s’attend en général à 200 (affichage du formulaire)
    assert response.status_code == 200

@pytest.mark.django_db
@test_id("TC003")
def test_delete_task_url(client):
    task = Task.objects.create(title="Task to delete")

    url = reverse("delete_task", args=[task.id])
    response = client.get(url)

    # Delete redirige souvent -> 302
    assert response.status_code in (200, 302)
