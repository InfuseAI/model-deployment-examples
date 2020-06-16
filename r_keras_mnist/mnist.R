reticulate::py_config()
library(keras)

predict.mnist <- function(mnist,newdata=list()) {
  cn <- 1:784
  for (i in seq_along(cn)){cn[i] <- paste("X",cn[i],sep = "")}
  colnames(newdata) <- cn
  predict(mnist$model, array_reshape(as.numeric(unlist(t(newdata), use.names=FALSE)), c(nrow(newdata), 28, 28, 1)))
}

send_feedback.mnist <- function(mnist,request=list(),reward=1,truth=list()) {
}

new_mnist <- function(filename) {
  model <- load_model_hdf5(filename)
  structure(list(model=model), class = "mnist")
}

initialise_seldon <- function(params) {
  new_mnist("model.h5")
}
