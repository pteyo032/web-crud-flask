from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import init_db, tout_lire, lire_un, creer, modifier, supprimer


def creer_app() -> Flask:
    app = Flask(__name__)

    # Initialisation de la base de données
    with app.app_context():
        init_db()

    # Routes HTML
    @app.get("/")
    def accueil():
        elements = tout_lire()
        return render_template("index.html", elements=elements)

    @app.post("/creer")
    def creer_post():
        titre = request.form.get("titre", "").strip()
        details = request.form.get("details", "").strip()
        if titre:
            creer(titre, details)
        return redirect(url_for("accueil"))

    @app.get("/modifier/<int:element_id>")
    def modifier_get(element_id: int):
        element = lire_un(element_id)
        if not element:
            return redirect(url_for("accueil"))
        return render_template("modifier.html", element=element)

    @app.post("/modifier/<int:element_id>")
    def modifier_post(element_id: int):
        titre = request.form.get("titre", "").strip()
        details = request.form.get("details", "").strip()
        if titre:
            modifier(element_id, titre, details)
        return redirect(url_for("accueil"))

    @app.post("/supprimer/<int:element_id>")
    def supprimer_post(element_id: int):
        supprimer(element_id)
        return redirect(url_for("accueil"))

    # API JSON (REST)
    @app.get("/api/elements")
    def api_lister():
        elements = tout_lire()
        return jsonify(elements), 200

    @app.get("/api/elements/<int:element_id>")
    def api_lire_un(element_id: int):
        element = lire_un(element_id)
        if not element:
            return jsonify({"erreur": "Élément introuvable"}), 404
        return jsonify(element), 200

    @app.post("/api/elements")
    def api_creer():
        data = request.get_json(silent=True) or {}
        titre = (data.get("titre") or "").strip()
        details = (data.get("details") or "").strip()

        if not titre:
            return jsonify({"erreur": "Le champ 'titre' est requis"}), 400
        if len(titre) > 80:
            return jsonify({"erreur": "Le titre doit faire 80 caractères max"}), 400
        if len(details) > 300:
            return jsonify({"erreur": "Les détails doivent faire 300 caractères max"}), 400

        creer(titre, details)
        return jsonify({"message": "Créé", "titre": titre, "details": details}), 201

    @app.put("/api/elements/<int:element_id>")
    def api_modifier(element_id: int):
        if not lire_un(element_id):
            return jsonify({"erreur": "Élément introuvable"}), 404

        data = request.get_json(silent=True) or {}
        titre = (data.get("titre") or "").strip()
        details = (data.get("details") or "").strip()

        if not titre:
            return jsonify({"erreur": "Le champ 'titre' est requis"}), 400
        if len(titre) > 80:
            return jsonify({"erreur": "Le titre doit faire 80 caractères max"}), 400
        if len(details) > 300:
            return jsonify({"erreur": "Les détails doivent faire 300 caractères max"}), 400

        modifier(element_id, titre, details)
        return jsonify({"message": "Modifié"}), 200

    @app.delete("/api/elements/<int:element_id>")
    def api_supprimer(element_id: int):
        if not lire_un(element_id):
            return jsonify({"erreur": "Élément introuvable"}), 404

        supprimer(element_id)
        return jsonify({"message": "Supprimé"}), 200

    # Gestion des erreurs (404)
    @app.errorhandler(404)
    def page_introuvable(_):
        if request.path.startswith("/api/"):
            return jsonify({"erreur": "Route introuvable"}), 404
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    app = creer_app()
    app.run(debug=True)
