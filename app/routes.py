"""Web and JSON API routes."""
import random
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from app import db
from app.models import Case, Vote
from app.statistics import get_case_statistics, format_sentence

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Show a random case."""
    cases = Case.query.order_by(Case.id.asc()).all()
    if not cases:
        return render_template("index.html", case=None)
    case = random.choice(cases)
    return render_template("index.html", case=case)


@main_bp.get("/result/<int:case_id>")
def result(case_id):
    """Show the latest guess saved by this browser and the real/user averages."""
    case = db.session.get(Case, case_id)
    if case is None:
        return render_template("404.html"), 404

    vote_id = session.get("last_vote_id")
    vote = db.session.get(Vote, vote_id) if vote_id else None
    if vote is None or vote.case_id != case.id:
        vote = (
            Vote.query.filter_by(case_id=case.id)
            .order_by(Vote.timestamp.desc(), Vote.id.desc())
            .first()
        )

    stats = get_case_statistics(case)
    your_fine = vote.fine_guess if vote else 0
    your_jail = vote.jail_guess if vote else 0
    return render_template(
        "result.html",
        case=case,
        stats=stats,
        your_fine=your_fine,
        your_jail=your_jail,
        your_sentence=format_sentence(your_fine, your_jail),
        real_sentence=format_sentence(case.real_fine, case.real_jail)
        if case.real_fine or case.real_jail else case.real_sentence,
        average_sentence=format_sentence(stats["average_fine"], stats["average_jail"]),
    )


@main_bp.post("/api/vote")
def api_vote():
    """Validate and save a guess, then redirect browsers to the result page."""
    case_id = request.form.get("case_id", type=int)
    fine_guess = request.form.get("fine_guess", type=float)
    jail_guess = request.form.get("jail_guess", type=float)
    case = db.session.get(Case, case_id) if case_id else None

    if case is None or fine_guess is None or jail_guess is None:
        return jsonify({"error": "Bitte wähle einen Fall und gib beide Schätzungen an."}), 400
    if not (0 <= fine_guess <= 5000 and 0 <= jail_guess <= 10):
        return jsonify({"error": "Die Werte liegen außerhalb des erlaubten Bereichs."}), 400

    vote = Vote(case_id=case.id, fine_guess=round(fine_guess, 2), jail_guess=round(jail_guess, 2))
    db.session.add(vote)
    db.session.commit()
    session["last_vote_id"] = vote.id
    return redirect(url_for("main.result", case_id=case.id), code=303)


@main_bp.get("/api/stats/<int:case_id>")
def api_stats(case_id):
    """Return aggregate statistics as JSON."""
    case = db.session.get(Case, case_id)
    if case is None:
        return jsonify({"error": "Fall nicht gefunden."}), 404
    stats = get_case_statistics(case)
    stats["average_sentence"] = format_sentence(stats["average_fine"], stats["average_jail"])
    return jsonify(stats)


@main_bp.get("/health")
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"})
