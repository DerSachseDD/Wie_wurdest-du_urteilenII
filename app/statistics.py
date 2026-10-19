"""Statistics and average calculations, kept separate from route handlers."""
from sqlalchemy import func
from app.models import Vote


def get_case_statistics(case):
    """Return vote count and average fine/jail guesses for a case."""
    result = (
        Vote.query.with_entities(
            func.count(Vote.id),
            func.avg(Vote.fine_guess),
            func.avg(Vote.jail_guess),
        )
        .filter(Vote.case_id == case.id)
        .one()
    )
    count, average_fine, average_jail = result
    return {
        "case_id": case.id,
        "vote_count": count or 0,
        "average_fine": round(float(average_fine or 0), 2),
        "average_jail": round(float(average_jail or 0), 2),
        "real_fine": case.real_fine,
        "real_jail": case.real_jail,
        "real_sentence": case.real_sentence,
    }


def format_sentence(fine, jail):
    """Format a fine/jail pair into readable German."""
    parts = []
    if fine and fine > 0:
        parts.append(f"{fine:,.0f} € Geldstrafe".replace(",", "."))
    if jail and jail > 0:
        parts.append(f"{jail:g} Jahre Freiheitsstrafe")
    return " und ".join(parts) if parts else "Keine Geld- oder Freiheitsstrafe"
