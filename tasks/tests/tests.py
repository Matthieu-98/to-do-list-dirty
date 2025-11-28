import pytest
from django.urls import reverse
from tasks.models import Task

@pytest.mark.django_db
def test_homepage_access(client):
    """La page d'accueil doit répondre 200."""
    url = reverse("home")   # si ton URL s'appelle différemment, adapte
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_task_url(client):
    """Test que la page de mise à jour répond bien."""
    # Création d’une tâche pour disposer d’un ID valide
    task = Task.objects.create(title="Test task")

    url = reverse("update_task", args=[task.id])
    response = client.get(url)

    # On s’attend en général à 200 (affichage du formulaire)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_task_url(client):
    """Test que la page de suppression est accessible."""
    task = Task.objects.create(title="Task to delete")

    url = reverse("delete_task", args=[task.id])
    response = client.get(url)

    # Delete redirige souvent -> 302
    assert response.status_code in (200, 302)
