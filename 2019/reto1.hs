import Data.List (elemIndex)
import Data.Maybe (fromJust)
import Data.Char (ord)

-- Transforma un número en una lista de dígitos. Ex: digitos 1592 == [1,5,9,2]
digitos :: Int -> [Int]
digitos =  map (read . (:[])) . show

-- Abecedario (con ñ)
abc :: String
abc = "abcdefghijklmnñopqrstuvwxyz"

-- Diferencia absoluta entre letras en el abecedario. Ex: diff c a == 2 
diff :: Char -> Char -> Int
diff x y = abs $ fromJust (elemIndex y abc) - fromJust (elemIndex x abc)

-- Duplica las letras tantas veces como diferencia de espacio entre la letra actual y la letra siguiente.
-- La última letra se compara con la primera.
-- Ex: paso0 "casa" == "ccaaaaaaaaaaaaaaaaaaasssssssssssssssssssaa"  
paso0 ::  String -> String
paso0 xs = concatMap (\(x, y) -> replicate (diff x y) x) (zip xs (tail xs ++ [head xs]))

-- Convierte todas las letras a su código ASCII y suma sus dígitos módulo 10
paso1 :: String -> [Int]
paso1 = map ((\x -> x `mod` 10) . sum . digitos . ord)

-- Dividimos la lista de números en grupos que comparten el mismo número contiguo.
-- Nos quedamos sólo con la cantidad de elementos (como máximo) que coincida con el número que contiene el elemento.
-- Ex: paso2 [2,2,2,3,2,2,2] == [2,2,3,2,2]
paso2 :: [Int] -> [Int]
paso2 [] = []
paso2 (0:xs) = 0 : paso2 (dropWhile (==0) xs)
paso2 xs@(x:_) = (take x ss) ++ paso2 rs
    where (ss,rs) = span (==x) xs

-- Agrupamos los números en grupos de 5, rellenando con 0 si no se alcanza a 5
paso3 :: [Int] -> [[Int]]
paso3 (x:y:z:w:e:xs) = [x,y,z,w,e] : paso3 xs
paso3 [] = []
paso3 y = [y ++ (replicate (5-(length y)) 0)]

-- Suma cada grupo módulo 16 y concatena los resultados
paso4 :: [[Int]] -> Int
paso4 = read . concat . map (show . (\x -> x `mod` 16) . sum)

-- Solución del reto1
reto1 :: String -> Int
reto1 = paso4 . paso3 . paso2 . paso1 . paso0