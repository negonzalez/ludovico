;; FILE: charlemagne.lsp
;; AUTHOR: Bob Green, rgreen@world.std.com
;; DATE: circa 1996

;; Copyright (c) 2001 Bob Green
;; All rights reserved.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;                  "Just by chance you crossed a diamond with a pearl.
;;                   You turned it on the world.  That's when you turned
;;                   the world around."
;;                                                         -- Steely Dan
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; debug info
(defconstant trace 0)

;;
(defvar CONSTANT-SYNTHESIS 0.0)

;; default value for safe functions
(defconstant safe-default 0)

;; safe division
(defun % (numerator denominator)
    (if (and (and (numberp numerator) (numberp denominator))
             (>= (* (abs (- 0 denominator)) 10000000000) 1))
        (/ numerator denominator)
        safe-default))

;;
(defun ^ (x y)
    (if (eq y 0)
        1.0
        (* x (^ x (- y 1)))))

;;
(defun depth (p)
    (cond
        ((atom p) 0)
        (t (max (+ 1 (depth (car p))) (depth (cdr p))))))
        
;; returns the number of arguments function f takes
;; returns -1 if it is not a genetically usable function
(defun num-args (f one-arg two-arg)
    (cond
        ((member f one-arg) 1)
        ((member f two-arg) 2)
        (t -1)))

;;
(defun ith-member (l i)
    (if (eq i 1) (car l) (ith-member (cdr l) (- i 1))))

;;
(defun random-elem (l)
    (ith-member l (+ 1 (random (length l)))))

;; create a random program
(defun random-program (max-depth terminals one-arg two-arg)
    (let ((non-terminals (append one-arg two-arg)))
        (let ((vocab (append terminals non-terminals)))
            (if (eq max-depth 1)
                (random-elem terminals)
                (let ((cur-node (random-elem vocab)))
                    (if (member cur-node terminals)
                        cur-node
                        (cons cur-node (random-program-list (num-args cur-node one-arg two-arg) (- max-depth 1) terminals one-arg two-arg))))))))

;; returns a list of random programs (branches) where n is the number of programs in the list and
;; max-depth is the maximum possible depth of each program if n=-1, it returns a list with a random
;; number of programs (at most the globally defined max-arg)
(defun random-program-list (n max-depth terminals one-arg two-arg)
    (cond ((eq n -1) (random-program-list (+ 1 (random max-arg)) max-depth) terminals one-arg two-arg)
        ((eq n 0) '())
        (t (cons (random-program max-depth terminals one-arg two-arg)
                     (random-program-list (- n 1) max-depth terminals one-arg two-arg)))))

;; return the number of atoms in the list at all layers
(defun flat-count (l)
    (cond
        ((eq l '()) 0)
        ((atom l) 1)
        ((atom (car l)) (+ 1 (flat-count (cdr l))))
        (t (+ (flat-count (car l)) (flat-count (cdr l))))))

;;
(defun 1st-branch (tree)
    (cond ((atom tree) '())
        (t (cadr tree))))

;;
(defun 2nd-branch (tree)
    (cond ((atom tree) '())
        ((null (cdr tree)) '())
        (t (caddr tree))))

;;
(defun 3rd-branch (tree)
    (cond ((atom tree) '())
        ((null (cdr tree)) '())
        ((null (cddr tree)) '())
        (t (cadddr tree))))

;; randomly mutates a single node in a program
(defun mutate (program n terminals one-arg two-arg)
    (let
        ((mutant (mutate-node program (random (flat-count program)) terminals one-arg two-arg)))
            (progn
                (if (>= trace 3) (print (list 'original program 'mutant mutant)))
                mutant)))

;; returns a program with the specified node n's program branch mutated
(defun mutate-node (p n terminals one-arg two-arg)
    (cond ((null p) '())
        ((<= n 1) (random-program (flat-count p) terminals one-arg two-arg))
        ((atom p) p)
        (t (nlist (list (car p)
                        (mutate-node (1st-branch p) (- n 1) terminals one-arg two-arg)
                        (mutate-node (2nd-branch p) (- n (+ 1 (flat-count (1st-branch p)))) terminals one-arg two-arg)
                        (mutate-node (3rd-branch p) (- n (+ 1 (+ (flat-count (1st-branch p))
                                                                 (flat-count (2nd-branch p))))) terminals one-arg two-arg))))))

;; returns the branch at the nth node as counted depth first
(defun flat-get-branch (n tree)
    (cond ((eq n 1) tree)
        ((<= (- n 1) (flat-count (1st-branch tree))) (flat-get-branch (- n 1) (1st-branch tree)))
        ((<= (- n 1) (+ (flat-count (1st-branch tree)) (flat-count (2nd-branch tree))))
           (flat-get-branch (- n (+ 1 (flat-count (1st-branch tree)))) (2nd-branch tree)))
        (t (flat-get-branch (- n (+ 1 (+ (flat-count (1st-branch tree))
                                    (flat-count (2nd-branch tree)))))
                       (3rd-branch tree)))))

;; returns the branch at the path specified
(defun path-get-branch (p path)
    (cond
        ((eq path '()) p)
        ((eq (car path) 0)
            (path-get-branch (cadr p) (cdr path)))
        (t (path-get-branch (caddr p) (cdr path)))))

(defun path-exists (p path)
    (cond
        ((eq path '()) T)
        ((atom p) NIL)
        ((eq (car path) 0)
            (if (eq (cdr p) '())
                NIL
                (path-exists (cadr p) (cdr path))))
        ((eq (car path) 1)
            (if (eq (cddr p) '())
                NIL
                (path-exists (caddr p) (cdr path))))))

;; changes the nth branch of tree as counted depth first to new-branch
(defun set-branch (n tree new-branch)
    (cond ((eq n 1) new-branch)
        ((<= (- n 1) (flat-count (1st-branch tree)))
           (cons (car tree) (nlist (list (set-branch (- n 1) (1st-branch tree) new-branch)
                                         (2nd-branch tree)
                                         (3rd-branch tree)))))
        ((<= (- n 1) (+ (flat-count (1st-branch tree)) (flat-count (2nd-branch tree))))
           (cons (car tree) (nlist (list (1st-branch tree)
                                         (set-branch (- n (+ 1 (flat-count (1st-branch tree))))
                                                     (2nd-branch tree)

                                                     new-branch)
                                         (3rd-branch tree)))))
        (t (cons (car tree) (nlist (list (1st-branch tree)
                                         (2nd-branch tree)
                                         (set-branch (- n (+ 1 (+ (flat-count (1st-branch tree))
                                                                  (flat-count (2nd-branch tree)))))
                                                     (3rd-branch tree)
                                                     new-branch)))))))

;; performs the crossover operation with the specified programs at the specified
;; depth first counted branches.  returns a list of the two children
(defun crossover-at (p1 p2 branch1 branch2)
    (let ((children
        (let ((copy-p1 p1)
               (i (+ 1 branch1))
               (j (+ 1 branch2)))
            (list (set-branch i p1 (flat-get-branch j p2))
                   (set-branch j p2 (flat-get-branch i copy-p1))))))
        (progn
            (if (>= trace 3) (print (list 'parent1 p1 'parent2 p2 'children children)) '())
            children)))

;; performs a context sensitive crossover operation at the specified path
;; returns a list of the two children
(defun context-sensitive-crossover-at (p1 p2 path)
    (list
        (context-sensitive-crossover-at-helper p1 p2 path)
        (context-sensitive-crossover-at-helper p2 p1 path)))

;;---original---
(defun context-sensitive-crossover-at-helper (p1 p2 path)
    (cond
        ((eq path '())
            p2)
        ((eq (car path) 0)
            (cons
                (car p1)
                (list
                    (context-sensitive-crossover-at-helper
                        (cadr p1)
                        (cadr p2)
                        (cdr path))
                    (caddr p1))))
        (t
            (cons
                (car p1)
                (list
                    (cadr p1)
                    (context-sensitive-crossover-at-helper
                        (caddr p1)
                        (caddr p2)
                        (cdr path)))))))
;;---original---


;; helper for context-sensitive-crossover-at function
(defun context-sensitive-crossover-at-helper (p1 p2 path)
    (cond
        ((eq path '())
            p2)
        ((eq (car path) 0)
            (cons
                (car p1)
                (nlist
                    (list
                        (context-sensitive-crossover-at-helper
                            (cadr p1)
                            (cadr p2)
                            (cdr path))
                        (caddr p1)))))
        (t
            (cons
                (car p1)
                (nlist
                    (list
                        (cadr p1)
                        (context-sensitive-crossover-at-helper
                            (caddr p1)
                            (caddr p2)
                            (cdr path))))))))

;; converts the flatcount n to a path like (0 1 1 0 0 1)
(defun tree-path (n p)
    (if (<= n 1)
        '()
        (cond
            ((<= (- n 1) (flat-count (1st-branch p)))
                (cons
                    '0
                    (tree-path
                        (- n 1)
                        (1st-branch p))))
            ((<= (- n 1) (+ (flat-count (1st-branch p))
                            (flat-count (2nd-branch p))))
                (cons
                    '1
                    (tree-path
                        (- n (+ 1 (+ (flat-count (1st-branch p)))))
                        (2nd-branch p))))
            (t '()))))

;; removes '()/NIL entries from a list
(defun nlist (items)
   (if (not (null (car items))) (cons (car items) (nlist (cdr items)))))



