module Tree (BinaryTree, insert, lookup, delete) where
import Prelude hiding (lookup)

data BinaryTree key value = Empty | Node key value (BinaryTree key value) (BinaryTree key value) deriving Show

lookup :: Ord key => key -> BinaryTree key value -> Maybe value
lookup _ Empty = Nothing
lookup key (Node node_key value left right) 
			| key == node_key = Just value
			| key < node_key = lookup key left
			| otherwise = lookup key right

insert :: Ord key => key -> value -> BinaryTree key value -> BinaryTree key value
insert key value Empty = Node key value Empty Empty
insert key value (Node node_key node_value left right) 
			| key == node_key = Node key value left right
			| key < node_key = Node node_key node_value (insert key value left) right
			| otherwise = Node node_key node_value left (insert key value right)

merge :: BinaryTree key value -> BinaryTree key value -> BinaryTree key value
merge tree Empty = tree
merge Empty tree = tree
merge tree (Node key value left right) = Node key value (merge tree left) right

delete :: Ord key => key -> BinaryTree key value -> BinaryTree key value
delete _ Empty = Empty
delete key (Node node_key node_value left right) 
			| key == node_key = merge left right
			| key < node_key = Node node_key node_value (delete key left) right
			| otherwise = Node node_key node_value left (delete key right)

