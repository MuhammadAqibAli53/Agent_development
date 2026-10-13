"""Run the three-agent internship matcher from the command line."""
import argparse

from cli_multi_agent.pipeline import run_internship_pipeline

DEFAULT_REQUEST = (
    "Find up to 3 Python internships in Lahore, Pakistan, suitable for my resume. "
    "Show which required skills are missing from my resume and save the shortlist."
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", default=DEFAULT_REQUEST, help="Internship role and location to search")
    args = parser.parse_args()
    try:
        state = run_internship_pipeline(args.request)
    except Exception as exc:
        print(f"Pipeline failed ({type(exc).__name__}). Check configuration, model access and connection.")
        return 1
    if state.get("error"):
        print(state["error"])
        return 1
    print("\nFINAL INTERNSHIP REPORT\n")
    print(state["report"])
    if state.get("saved_to"):
        print("\nSaved to:", state["saved_to"])
    if state.get("save_error"):
        print("\nSave error:", state["save_error"])
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
