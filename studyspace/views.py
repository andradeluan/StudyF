from django.shortcuts import render, redirect,get_object_or_404
from .models import CardVideo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from .models import CardVideo
import json

# Configurar cliente da OpenAI(KEY API)
client = OpenAI(api_key="SUA CHAVE API DA OPENAI")

@csrf_exempt
@login_required
def studyspace(request):
    # Obtém o username diretamente do usuário autenticado
    username = request.user.username if request.user.is_authenticated else None
    
    # Filtra os cards do usuário logado
    user_cards = CardVideo.objects.filter(user=request.user)
    
    # Passa um único dicionário como contexto
    context = {
        'cards': user_cards,
        'username': username,
    }
    return render(request, 'studyspace/studyspace.html', context)
  

@csrf_exempt
@login_required
def create_card(request):
    if request.method == 'POST':
      youtube_url = request.POST.get('youtubeUrl')
      video_language = request.POST.get('videoLanguage')
      title = request.POST.get('titleUrl')
      id_video = YouTube(youtube_url).video_id
      
      legenda = get_captions(id_video, video_language)
      
      resumo = summarize_transcript(legenda)
      roteiro = roadmap_transcript(legenda)
      flashcards = flashcards_transcript(legenda)

      # Criação do CardVideo com associação ao usuário
      card = CardVideo(
          id_video=id_video,  
          user=request.user,
          titulo=title, 
          resumo=resumo,
          roteiro_estudos=roteiro,
          flashcards=flashcards)
      card.save()
      
      return redirect('card',id_video = id_video)

      
def get_captions(video_id, video_language):
    if video_language == 'pt':
      primary_language = 'pt'
      fallback_language = 'en'
    elif video_language == 'en':
      primary_language = 'en'
      fallback_language = 'pt'
  
    try:
        # Tenta obter as legendas no idioma primário
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[primary_language])
        captions = " ".join(entry['text'] for entry in transcript)
        return captions
    except:
        try:
            # Se falhar, tenta obter as legendas no idioma alternativo
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[fallback_language])
            captions = " ".join(entry['text'] for entry in transcript)
            return captions
        except Exception as e:
            return f"Erro ao obter legendas: {e}"
  
  
def summarize_transcript(transcript):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Resuma o seguinte texto da melhor forma possivel deixando um resumo muito claro:"},
            {"role": "user", "content": transcript}
        ]
    )
    return completion.choices[0].message.content
  
  
def roadmap_transcript(transcript):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Crie um roadmap com base nesse texto de forma clara e resumida:"},
            {"role": "user", "content": transcript}
        ]
    )
    return completion.choices[0].message.content


def flashcards_transcript(transcript):
    
    completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Create a list of flashcards in JSON format from the following text. "
                        "Each flashcard should have a 'question' and an 'answer'. "
                        "The response should be a JSON array of objects with 'question' and 'answer' fields only.  e nada de ```json``` and /n"
                        "Here is the text:"
                    )
                },
                {"role": "user", "content": transcript}
            ]
        )
    return completion.choices[0].message.content

@csrf_exempt
@login_required
def card(request,id_video):
    user_card = get_object_or_404(CardVideo, id_video=id_video, user_id=request.user)

    # Decodificar o campo JSON dos flashcards
    flashcards = json.loads(user_card.flashcards) if user_card.flashcards else []

    # Obtém o username diretamente do usuário autenticado
    username = request.user.username if request.user.is_authenticated else None
    context = {
        'titulo': user_card.titulo,
        'resumo': user_card.resumo,
        'roteiro_estudos': user_card.roteiro_estudos,
        'flashcards': flashcards,
        'username': username,
    }
    return render(request,'studyspace/card.html',context)


@csrf_exempt
@login_required
def delete_card(request, id_video):
    try:
        card = CardVideo.objects.get(id_video=id_video, user=request.user)
        card.delete()
        return JsonResponse({'status': 'success', 'message': 'Card excluído com sucesso!'})
    except CardVideo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Card não encontrado!'}, status=404)
    
