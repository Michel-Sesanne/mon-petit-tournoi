document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-preparation');
    const tirageContainer = document.getElementById('tirage-poules');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const selected = Array.from(form.querySelectorAll('input[name="joueurs"]:checked'));
        if (selected.length < 6) {
            alert("Sélectionnez au moins 6 joueurs.");
            return;
        }

        const joueursData = selected.map(input => {
            const id = input.value;
            const equipeInput = form.querySelector(`input[name="equipe_${id}"]`);
            const equipe = equipeInput.value.trim();
            if (!equipe) throw new Error("Chaque joueur doit avoir une équipe.");
            return { id, equipe };
        });

        const tournoiId = window.location.pathname.split('/').pop();

        // Appel serveur pour effectuer le tirage
        try {
            const response = await fetch(`/tirage_tournoi/${tournoiId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ joueurs: joueursData })
            });
            if (!response.ok) throw new Error("Erreur lors du tirage.");

            const data = await response.json();

            // Affichage des poules
            tirageContainer.innerHTML = '';
            data.poules.forEach(poule => {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${poule.nom}</strong>: ${poule.joueurs.map(j => j.nom + ' (' + j.equipe + ')').join(', ')}`;
                tirageContainer.appendChild(div);
            });

            // Optionnel : redirection vers tournoi.html après 2s
            setTimeout(() => {
                window.location.href = `/tournoi/${tournoiId}`;
            }, 2000);
        } catch (err) {
            alert(err.message);
        }
    });
});
