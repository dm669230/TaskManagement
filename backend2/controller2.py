from fastapi import FastAPI, Depends, HTTPException
from backend2.models import Tasks
import pandas as pd
from io import BytesIO
from starlette.responses import StreamingResponse
import traceback


def get_task(db):
    try:
        # Fetch all tasks and convert to list of dicts
        tasks = db.query(Tasks).all()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found.")

        # Convert to DataFrame
        df = pd.DataFrame([task.__dict__ for task in tasks])
        df.drop(columns=["_sa_instance_state"], errors="ignore", inplace=True)

        # Write to Excel in memory
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name="Tasks")
        output.seek(0)

        # Stream Excel file as response
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=tasks.xlsx"}
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


