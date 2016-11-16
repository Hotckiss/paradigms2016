module Fp1 where

head' :: [a] -> a
head' (x:xs) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (x:xs) = xs

take' :: Int -> [a] -> [a]
take' 0 _ = []
take' _ [] = []
take' n (x:xs) = x : (take' (n-1) xs)

drop' :: Int -> [a] -> [a]
drop' 0 (x:xs) = (x:xs)
drop' _ [] = []
drop' n (x:xs) = (drop' (n-1) xs)

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' f (x:xs) = if (f x) then (x:filter' f xs) else (filter' f xs)

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' (x:xs) [] = (x:xs)
concat' [] (y:ys) = (y:ys)
concat' (x:xs) (y:ys) = x : concat' xs (y:ys)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = concat' (concat' (quickSort' (filter' (< x) xs ) ) (filter' (== x) (x:xs)) ) (quickSort' (filter' (> x) xs ) )


