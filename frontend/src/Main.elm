module Main exposing (..)

import Browser
import Html exposing (Html, Attribute, div, input, text, h1)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)

import Element exposing (Element, rgb, el, row, alignRight, fill, width, rgb255, spacing, centerY, padding)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input as InputEl

main =
  Browser.sandbox { init = init, update = update, view = view }

type Msg =
  SearchInput String

type alias Model =
  {
    content : String
  }

init : Model
init =
  {
    content = ""
  }

update msg model =
  case msg of
    SearchInput inputData ->
      {model | content = inputData}

view : Model -> Html Msg
view model =
  Element.layout []
  <|
    Element.el
    [Font.family
      [Font.external
          { url = "https://fonts.googleapis.com/css?family=EB+Garamond",
          name = "EB Garamond"
          },
        Font.sansSerif
      ],
      Font.size 50,
      padding 10
    ]
    (Element.text "Gutenberg Library")

  -- div []
  --   [
  --   div [] [h1 [] [text "Gutenberg Library"]],
  --   input [ placeholder "Text to reverse", value model.content, onInput SearchInput ] [],
  --   div [] [ text (String.reverse model.content) ]
  --   ]
