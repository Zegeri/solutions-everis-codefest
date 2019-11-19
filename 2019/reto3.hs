import Data.List (group)
import Control.Monad (guard)

-- Transforma un número en una lista de dígitos. Ex: digitos 1592 == [1,5,9,2]
digitos :: Int -> [Int]
digitos =  map (read . (:[])) . show

-- Transforma número 0-9 a Char '0'-'9'.
num2char :: Int -> Char
num2char = head . show

cifrar :: Int -> Int
cifrar = read . concat . map (\xs -> show (length xs * 10 + head xs)) . group . digitos

descifrar :: Int -> Maybe Int
descifrar x = do
  let xs = digitos x
  guard (length xs `mod` 2 == 0)
  let desc = read $ aux xs
  guard (cifrar desc == x)
  guard (desc /= x)
  return desc

-- Paso auxiliar en el descifrado. Ex: [1,3,2,5] = "355"
aux :: [Int] -> String
aux (x:y:xs) = (replicate x (num2char y)) ++ aux xs
aux [] = ""

-- Repite f reiteradamente hasta devolver Nothing
iter :: (a -> Maybe a) -> a -> [a]
iter f x = x : (case f x of
  Nothing -> []
  Just y -> iter f y)

reto3 :: Int -> Int
reto3 x = last (iter descifrar x)