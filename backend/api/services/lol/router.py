from typing import List
from fastapi import APIRouter, HTTPException
from api.services.lol.models import LOLMatch
from api.services.lol import actions

router = APIRouter(prefix="/matches")

# Создание матча


# @router.post("/", response_model=Match)
# def create_match(match: MatchCreate):
#     return actions.create_match(match)

# Получение всех матчей


@router.get("/", response_model=List[LOLMatch])
def get_all_matches():
    matches = actions.get_matches()
    return matches

# Получение матча по ID


# @router.get("/{match_id}", response_model=Match)
# def get_match_by_id(match_id: str):
#     match = actions.get_match_by_id(match_id)
#     if match:
#         return match
#     else:
#         raise HTTPException(status_code=404, detail="Match not found")

# # Обновление матча


# @router.put("/{match_id}", response_model=Match)
# def update_match(match_id: str, match: MatchUpdate):
#     return actions.update_match(match_id, match)

# # Удаление матча


# @router.delete("/{match_id}", status_code=201)
# def delete_match(match_id: str):
#     actions.delete_match(match_id)
